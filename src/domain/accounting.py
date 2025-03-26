from typing import Optional

from controls import utils, controls
from db import Repository
from domain.types import CategoriesUpdater
from domain.types.accounting_types import ChangeUsername, ChangePassword, GetAccount
from entities.account import Account


def get_account(user_id: int, offset: int) -> GetAccount:
    count = Repository.Accounting.count_of_accounts(user_id)
    if count == 0:
        return GetAccount(offset=offset)

    if offset >= count:
        offset = 0

    account = Repository.Accounting.get_account_by_offset(user_id, offset)
    return GetAccount(offset=offset, count=count, data=account)


async def create_account(user_id: int, username: str) -> Optional[Account]:
    if Repository.Accounting.is_username_exist(username):
        return None

    account = Account(username=username, password=utils.gen_password())
    account.position = controls.add_user(user_id, account.username, account.password)
    controls.update_hook()
    account.id = Repository.Accounting.add_account(user_id, account.position, account.username, account.password)

    # Commands and access lists
    count_of_accounts = Repository.Accounting.count_of_accounts(user_id)
    accounts_limit = Repository.Common.get_user(user_id).accounts_limit

    await CategoriesUpdater(user_id) \
        .can_create_account(count_of_accounts, accounts_limit) \
        .has_accounts(count_of_accounts) \
        .finish()

    return account


async def delete_account(user_id: int, account_id: int) -> bool:
    position = Repository.Accounting.get_account_position(user_id, account_id)
    if position is None:
        return False

    diff = controls.remove_user(user_id, position)
    if diff is None:
        raise Exception(f'Out of range {user_id}:{position}')

    controls.update_hook()

    if diff != 0:
        Repository.Accounting.move_accounts(user_id, position, diff)
    is_removed = Repository.Accounting.remove_account(user_id, account_id)

    # Commands and access lists
    accounts = Repository.Accounting.count_of_accounts(user_id)
    accounts_limit = Repository.Common.get_user(user_id).accounts_limit

    await CategoriesUpdater(user_id) \
        .can_create_account(accounts, accounts_limit) \
        .has_accounts(accounts) \
        .finish()

    return is_removed


def change_username(user_id: int, account_id: int, new_username: str) -> ChangeUsername:
    position = Repository.Accounting.get_account_position(user_id, account_id)
    if position is None:
        return ChangeUsername()

    if Repository.Accounting.is_username_exist(new_username):
        return ChangeUsername(username_exist=True)

    diff = controls.set_username(user_id, position, new_username)
    if diff is None:
        raise Exception(f'Out of range {user_id}:{position}')

    controls.update_hook()

    if diff != 0:
        Repository.Accounting.move_accounts(user_id, position, diff)

    changed = Repository.Accounting.set_username(user_id, account_id, new_username)
    return ChangeUsername(changed=changed, data=Repository.Accounting.get_account(user_id, account_id))


def reset_password(user_id: int, account_id: int) -> ChangePassword:
    position = Repository.Accounting.get_account_position(user_id, account_id)
    if position is None:
        return ChangePassword()

    password = utils.gen_password()
    diff = controls.set_password(user_id, position, password)
    if diff is None:
        raise Exception(f'Out of range {user_id}:{position}')

    controls.update_hook()

    if diff != 0:
        Repository.Accounting.move_accounts(user_id, position, diff)

    changed = Repository.Accounting.set_password(user_id, account_id, password)
    return ChangePassword(changed, Repository.Accounting.get_account(user_id, account_id))
