from database.accounts_abstract import Accounts
from database.base_sqlite import BaseSqlite, transaction


class AccountsSqlite(Accounts, BaseSqlite):
    @classmethod
    @transaction
    def create_table(cls, c):
        sql = 'CREATE TABLE IF NOT EXISTS accounts (' \
              'id INT not null, ' \
              'username TEXT not null, ' \
              'pos INT not null unique, ' \
              'PRIMARY KEY (id, username), ' \
              'FOREIGN KEY (id) REFERENCES users (id) on delete RESTRICT on update RESTRICT)'
        c.execute(sql)

    @classmethod
    @transaction
    def remove_username(cls, id: int, c) -> bool:
        sql = 'DELETE FROM accounts WHERE id = ? AND username = ?'
        params = (id, username)
        return bool(c.execute(sql, params).rowcount == 1)

    @classmethod
    @transaction
    def change_username(cls, id: int, new_username: str, c) -> bool:
        sql = 'UPDATE users SET username = ? WHERE id = ?'
        params = (new_username, id)
        return bool(c.execute(sql, params).rowcount == 1)

    @classmethod
    @transaction
    def change_pos(cls, *set: tuple[int, int], c) -> bool:
        sql = 'UPDATE users SET pos = ? WHERE id = ?'
        params = set
        return bool(c.executemany(sql, params).rowcount == len(set))
