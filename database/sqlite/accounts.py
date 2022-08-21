from database.abstract import Accounts
from .transaction import TransactionSqlite, transaction


class AccountsSqlite(Accounts):
    @classmethod
    @transaction
    def remove_username(cls, id: int, username: str, t: TransactionSqlite) -> bool:
        sql = 'DELETE FROM accounts WHERE id = ? AND username = ?'
        return t.update_one(sql, id, username)

    @classmethod
    @transaction
    def change_username(cls, id: int, username: str, new_username: str, t: TransactionSqlite) -> bool:
        sql = 'UPDATE accounts SET username = ? WHERE id = ? AND username = ?'
        return t.update_one(sql, new_username, id, username)

    @classmethod
    @transaction
    def change_pos(cls, *data: tuple[int, int], t: TransactionSqlite) -> bool:
        sql = 'UPDATE accounts SET pos = ? WHERE id = ?'
        return t.data.executemany(sql, data).rowcount == len(data)
