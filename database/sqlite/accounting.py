from typing import Optional

from entities.account import Account
from .connection import ConnectionSqlite
from ..abstract.accounting import Accounting


class AccountingSqlite(Accounting):

    @classmethod
    def get_account_position(cls, user_id: int, id: int, c: ConnectionSqlite = None) -> Optional[int]:
        sql = 'SELECT position FROM accounts WHERE ROWID = ? AND user_id = ?'
        return int(c.single(sql, id, user_id))

    @classmethod
    def get_account(cls, user_id: int, id: int, c: ConnectionSqlite = None) -> Optional[Account]:
        sql = 'SELECT ROWID, username, password FROM accounts WHERE ROWID = ? AND user_id = ?'
        r = c.fetch_one(sql, id, user_id)
        return None if r is None else Account(id=r[0], username=r[1], password=r[2])

    @classmethod
    def get_account_by_offset(cls, user_id: int, offset: int, c: ConnectionSqlite = None) -> Optional[Account]:
        sql = 'SELECT ROWID, username, password FROM accounts WHERE user_id = ? ORDER BY position LIMIT ?, 1'
        r = c.fetch_one(sql, user_id, offset)
        return None if r is None else Account(id=r[0], username=r[1], password=r[2])

    @classmethod
    def is_username_exist(cls, username: str, c: ConnectionSqlite = None) -> bool:
        return bool(c.single('SELECT COUNT(ROWID) > 0 FROM accounts WHERE username = ?', username))

    @classmethod
    def add_account(cls, user_id: int, position: int, username: str, password: str, c: ConnectionSqlite = None) -> int:
        sql = 'INSERT INTO accounts (user_id, position, username, password) VALUES (?, ?, ?, ?)'
        return c.insert_id(sql, user_id, position, username, password)

    @classmethod
    def set_username(cls, user_id: int, id: int, username: str, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE accounts SET username = ? WHERE user_id = ? AND ROWID = ?'
        return c.update_one(sql, username, user_id, id)

    @classmethod
    def set_password(cls, user_id: int, id: int, password: str, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE accounts SET password = ? WHERE user_id = ? AND ROWID = ?'
        return c.update_one(sql, password, user_id, id)

    @classmethod
    def move_accounts(cls, user_id: int, position: int, diff: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE accounts SET position = position + ? WHERE user_id = ? AND position > ?'
        return c.update_many(sql, diff, user_id, position)

    @classmethod
    def remove_account(cls, user_id: int, id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ? AND ROWID = ?'
        return c.update_one(sql, user_id, id)

    @classmethod
    def remove_all(cls, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ?'
        return c.update_many(sql, user_id)

    @classmethod
    def count_of_accounts(cls, user_id: int, c: ConnectionSqlite = None) -> int:
        sql = 'SELECT COUNT(ROWID) FROM accounts WHERE user_id = ?'
        return int(c.single(sql, user_id))

    @classmethod
    def get_next_account_data(cls, user_id: int, offset: int, c: ConnectionSqlite = None) -> tuple[int, int]:
        sql = 'SELECT ROWID, position FROM accounts WHERE user_id = ? ORDER BY position LIMIT ?, 1'
        return c.fetch_one(sql, user_id, offset)


accounting: Accounting = AccountingSqlite()
