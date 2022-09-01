from typing import Optional

import database
import domain.commands
from bot_commands.categories import Categories
from controls import utils, controls
from database.abstract import Connection
from entities.account import Account


def _fill(category: Categories, predicate: bool, append: set[Categories], remove: set[Categories]):
    if predicate:
        append.add(category)
        remove.discard(category)
    else:
        append.discard(category)
        remove.add(category)


def _get_account(user_id: int, id: int, position: int):
    user_data = controls.get_account(user_id, position)
    if user_data is not None:
        return Account(id, user_data[0], user_data[1])
    else:
        raise RuntimeError(f'Account {user_id}:{position} not found')


@database.connection()
def get_account(user_id: int, offset: int, c) -> Optional[tuple[int, int, Account]]:
    count = database.accounting.count_of_accounts(user_id, c)
    if count == 0:
        return None

    if offset >= count:
        offset = 0
    id, position = database.accounting.get_next_account_data(user_id, offset, c)
    return offset, count, _get_account(user_id, id, position)


@database.connection(manual=True)
async def create_account(user_id: int, username: str, c: Connection) -> Account:
    account = Account(username=username, password=utils.gen_password())
    account.position = controls.add_user(user_id, account.username, account.password)
    c.open()
    c.begin_transaction()
    account.id = database.accounting.add_account(user_id, account.position, c)

    # Commands and access lists
    user = database.common.get_user(user_id, c)
    accounts = database.accounting.count_of_accounts(user_id, c)
    append, remove = set(), set()

    _fill(Categories.CAN_CREATE_ACCOUNT, accounts < user.accounts_limit, append, remove)
    _fill(Categories.HAS_ACCOUNTS, accounts > 0, append, remove)

    await domain.commands.update(user_id, append, remove, c)
    c.end_transaction()

    c.close()
    return account


@database.connection(manual=True)
async def delete_account(user_id: int, id: int, c) -> bool:
    c.open()
    position = database.accounting.get_account_position(user_id, id, c)
    if position is None:
        c.close()
        return False

    diff = controls.remove_user(user_id, position)
    if diff is None:
        c.close()
        raise RuntimeError(f'Out of range {user_id}:{position}')

    c.begin_transaction()
    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    is_removed = database.accounting.remove_account(user_id, id, c)

    # Commands and access lists
    user = database.common.get_user(user_id, c)
    accounts = database.accounting.count_of_accounts(user_id, c)
    append, remove = set(), set()

    _fill(Categories.CAN_CREATE_ACCOUNT, accounts < user.accounts_limit, append, remove)
    _fill(Categories.HAS_ACCOUNTS, accounts > 0, append, remove)

    await domain.commands.update(user_id, append, remove, c)
    c.end_transaction()

    c.close()
    return is_removed


@database.connection()
def change_username(user_id: int, id: int, new_username: str, c) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id, c)
    if position is None:
        return None

    diff = controls.set_username(user_id, position, new_username)
    if diff is None:
        raise RuntimeError(f'Out of range {user_id}:{position}')

    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    return _get_account(user_id, id, position)


@database.connection()
def reset_password(user_id: int, id: int, c) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id, c)
    if position is None:
        return None

    password = utils.gen_password()
    diff = controls.set_password(user_id, position, password)
    if diff is None:
        raise RuntimeError(f'Out of range {user_id}:{position}')

    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    return _get_account(user_id, id, position)
