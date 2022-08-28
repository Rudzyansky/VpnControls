from typing import Optional

import database
from controls import utils, controls
from entities.account import Account


def get_account(user_id: int, id: int) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id)
    if position:
        user_data = controls.get_account(user_id, position)
        if user_data:
            return Account(id, user_data[0], user_data[1])
        else:
            raise RuntimeError(f'Account {user_id}:{position} not found')
    return None


def create_account(user_id: int, username: str) -> Account:
    account = Account(username=username, password=utils.gen_password())
    account.position = controls.add_user(user_id, account.username, account.password)
    account.id = database.accounting.add_account(user_id, account.position)
    return account


@database.connection()
def delete_account(user_id: int, id: int, c) -> bool:
    position = database.accounting.get_account_position(id, c)
    diff = controls.remove_user(user_id, position)
    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    database.accounting.remove_account(id, c)
    return True


@database.connection()
def change_username(user_id: int, id: int, new_username: str, c) -> Account:
    position = database.accounting.get_account_position(user_id, id, c)
    account = controls.get_account(user_id, id)
    account.username = new_username
    diff = controls.set_username(user_id, position, account.username)
    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    return account


@database.connection()
def reset_password(user_id: int, id: int, c) -> Account:
    position = database.accounting.get_account_position(user_id, id, c)
    account = controls.get_account(user_id, id)
    account.password = utils.gen_password()
    diff = controls.set_password(user_id, position, account.password)
    if diff != 0:
        database.accounting.move_accounts(user_id, position, diff, c)
    return account
