from database.accounts_abstract import Accounts
from database.base_sqlite import BaseSqlite


class AccountsSqlite(Accounts, BaseSqlite):
    @classmethod
    def create_table(cls):
        def func(c):
            sql = 'CREATE TABLE IF NOT EXISTS accounts (' \
                  'id INT not null, ' \
                  'username TEXT not null, ' \
                  'pos INT not null unique, ' \
                  'PRIMARY KEY (id, username), ' \
                  'FOREIGN KEY (id) REFERENCES users (id) on delete RESTRICT on update RESTRICT)'
            c.execute(sql)

        cls.transaction(func)

    @classmethod
    def remove_username(cls, id: int) -> bool:
        def func(c):
            sql = 'DELETE FROM accounts WHERE id = ? AND username = ?'
            params = (id, username)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)

    @classmethod
    def change_username(cls, id: int, new_username: str) -> bool:
        def func(c):
            sql = 'UPDATE users SET username = ? WHERE id = ?'
            params = (new_username, id)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)

    @classmethod
    def change_pos(cls, *set: tuple[int, int]) -> bool:
        def func(c):
            sql = 'UPDATE users SET pos = ? WHERE id = ?'
            params = set
            return bool(c.executemany(sql, params).rowcount == len(set))

        return cls.transaction(func)
