from typing import Optional

import database
from controls import utils, controls
from entities.account import Account


def _get_account(user_id: int, id: int, position: int):
    user_data = controls.get_account(user_id, position)
    if user_data:
        return Account(id, user_data[0], user_data[1])
    else:
        raise RuntimeError(f'Account {user_id}:{position} not found')


def get_account(user_id: int, id: int) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id)
    return _get_account(user_id, id, position) if position else None


def create_account(user_id: int, username: str) -> Account:
    account = Account(username=username, password=utils.gen_password())
    account.position = controls.add_user(user_id, account.username, account.password)
    account.id = database.accounting.add_account(user_id, account.position)
    return account


@database.connection()
def delete_account(user_id: int, id: int, c) -> bool:
    position = database.accounting.get_account_position(id, c)
    if position:
        diff = controls.remove_user(user_id, position)
        if diff:
            if diff != 0:
                database.accounting.move_accounts(user_id, position, diff, c)
            return database.accounting.remove_account(id, c)
        else:
            raise RuntimeError(f'Out of range {user_id}:{position}')
    return False


@database.connection()
def change_username(user_id: int, id: int, new_username: str, c) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id, c)
    if position:
        diff = controls.set_username(user_id, position, new_username)
        if diff:
            if diff != 0:
                database.accounting.move_accounts(user_id, position, diff, c)
            return _get_account(user_id, id, position)
        else:
            raise RuntimeError(f'Out of range {user_id}:{position}')
    return None


@database.connection()
def reset_password(user_id: int, id: int, c) -> Optional[Account]:
    position = database.accounting.get_account_position(user_id, id, c)
    if position:
        password = utils.gen_password()
        diff = controls.set_password(user_id, position, password)
        if diff:
            if diff != 0:
                database.accounting.move_accounts(user_id, position, diff, c)
            return _get_account(user_id, id, position)
        else:
            raise RuntimeError(f'Out of range {user_id}:{position}')
    return None
