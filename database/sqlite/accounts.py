from database.abstract import Accounts
from .connection import ConnectionSqlite, connection


class AccountsSqlite(Accounts):
    @classmethod
    @connection
    def remove_username(cls, id: int, username: str, c: ConnectionSqlite) -> bool:
        sql = 'DELETE FROM accounts WHERE id = ? AND username = ?'
        return c.update_one(sql, id, username)

    @classmethod
    @connection
    def change_username(cls, id: int, username: str, new_username: str, c: ConnectionSqlite) -> bool:
        sql = 'UPDATE accounts SET username = ? WHERE id = ? AND username = ?'
        return c.update_one(sql, new_username, id, username)

    @classmethod
    @connection
    def change_pos(cls, *data: tuple[int, int], c: ConnectionSqlite) -> bool:
        sql = 'UPDATE accounts SET pos = ? WHERE id = ?'
        return c.data.executemany(sql, data).rowcount == len(data)
