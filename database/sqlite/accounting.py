from typing import Optional

from .connection import ConnectionSqlite, connection
from ..abstract.accounting import Accounting


class AccountingSqlite(Accounting):

    @classmethod
    @connection(False)
    def get_account_position(cls, user_id: int, id: int, c: ConnectionSqlite = None) -> Optional[int]:
        sql = 'SELECT position FROM accounts WHERE ROWID = ? AND user_id = ?'
        return int(c.single(sql, id, user_id))

    @classmethod
    @connection()
    def add_account(cls, user_id: int, position: int, c: ConnectionSqlite = None) -> Optional[int]:
        sql = 'INSERT INTO accounts (user_id, position) VALUES (?, ?)'
        c.update_one(sql, user_id, position)
        return c.data.lastrowid

    @classmethod
    @connection()
    def move_accounts(cls, user_id: int, position: int, diff: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE accounts SET position = position + ? WHERE user_id = ? AND position > ?'
        return c.update_many(sql, diff, user_id, position)

    @classmethod
    def remove_account(cls, user_id: int, position: int, c: ConnectionSqlite = None) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ? AND position = ?'
        return c.update_many(sql, user_id, position)

    @classmethod
    @connection()
    def remove_all(cls, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ?'
        return c.update_many(sql, user_id)


accounting: Accounting = AccountingSqlite()