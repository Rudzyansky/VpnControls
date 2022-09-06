from typing import Optional

import database
from controls import utils, controls
from database.abstract import Connection
from domain.types import CategoriesUpdater
from domain.types.accounting_types import ChangeUsername, ChangePassword, GetAccount
from entities.account import Account


@database.connection(False)
def get_account(user_id: int, offset: int, c) -> GetAccount:
    count = database.accounting.count_of_accounts(user_id, c)
    if count == 0:
        return GetAccount(offset=offset)

    if offset >= count:
        offset = 0

    account = database.accounting.get_account_by_offset(user_id, offset, c)
    return GetAccount(offset=offset, count=count, data=account)


@database.connection(manual=True)
async def create_account(user_id: int, username: str, c: Connection) -> Optional[Account]:
    c.open()
    if database.accounting.is_username_exist(username, c):
        c.close()
        return None

    account = Account(username=username, password=utils.gen_password())
    c.begin_transaction()
    account.position = controls.add_user(user_id, account.username, account.password)
    controls.update_hook()
    account.id = database.accounting.add_account(user_id, account.position, account.username, account.password, c)

    # Commands and access lists
    count_of_accounts = database.accounting.count_of_accounts(user_id, c)
    accounts_limit = database.common.get_user(user_id, c).accounts_limit

    await CategoriesUpdater(user_id) \
        .can_create_account(count_of_accounts, accounts_limit) \
        .has_accounts(count_of_accounts) \
        .finish(c)

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

    controls.update_hook()

    c.begin_transaction()
    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    is_removed = database.accounting.remove_account(user_id, id, c)

    # Commands and access lists
    accounts = database.accounting.count_of_accounts(user_id, c)
    accounts_limit = database.common.get_user(user_id, c).accounts_limit

    await CategoriesUpdater(user_id) \
        .can_create_account(accounts, accounts_limit) \
        .has_accounts(accounts) \
        .finish(c)

    c.end_transaction()

    c.close()
    return is_removed


@database.connection()
def change_username(user_id: int, id: int, new_username: str, c) -> ChangeUsername:
    position = database.accounting.get_account_position(user_id, id, c)
    if position is None:
        return ChangeUsername()

    if database.accounting.is_username_exist(new_username, c):
        return ChangeUsername(username_exist=True)

    diff = controls.set_username(user_id, position, new_username)
    if diff is None:
        raise RuntimeError(f'Out of range {user_id}:{position}')

    controls.update_hook()

    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)

    changed = database.accounting.set_username(user_id, id, new_username, c)
    return ChangeUsername(changed=changed, data=database.accounting.get_account(user_id, id, c))


@database.connection()
def reset_password(user_id: int, id: int, c) -> ChangePassword:
    position = database.accounting.get_account_position(user_id, id, c)
    if position is None:
        return ChangePassword()

    password = utils.gen_password()
    diff = controls.set_password(user_id, position, password)
    if diff is None:
        raise RuntimeError(f'Out of range {user_id}:{position}')

    controls.update_hook()

    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)

    changed = database.accounting.set_password(user_id, id, password, c)
    return ChangePassword(changed, database.accounting.get_account(user_id, id, c))
