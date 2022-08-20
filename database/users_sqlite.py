from database.base_sqlite import BaseSqlite
from database.users_abstract import Users


class UsersSqlite(Users, BaseSqlite):
    @classmethod
    def create_table(cls):
        def func(c):
            sql = 'CREATE TABLE IF NOT EXISTS users (' \
                  'id INT primary key, ' \
                  'is_admin INT default 0, ' \
                  'accounts_limit INT default 1, ' \
                  'owner_id INT default NULL, ' \
                  'FOREIGN KEY (owner_id) REFERENCES users (id) on delete RESTRICT on update RESTRICT)'
            c.execute(sql)
            sql = 'CREATE VIEW IF NOT EXISTS slaves AS ' \
                  'WITH RECURSIVE slaves (leaf_id, id) AS (' \
                  'SELECT id, id FROM users UNION ALL ' \
                  'SELECT s.leaf_id, u.id FROM users u JOIN slaves s ON u.owner_id = s.id' \
                  ') SELECT * FROM slaves'
            c.execute(sql)

        cls.transaction(func)

    @classmethod
    def slaves(cls, id: int) -> list[int]:
        def func(c):
            sql = 'SELECT id FROM slaves WHERE leaf_id = ?'
            params = (id,)
            return [_id for _id, in c.execute(sql, params).fetchall()]

        return cls.transaction(func)

    @classmethod
    def fetch_all(cls) -> list[int]:
        def func(c):
            sql = 'SELECT id FROM users'
            return [id for id, in c.execute(sql).fetchall()]

        return cls.transaction(func)

    @classmethod
    def fetch_admins(cls) -> list[int]:
        def func(c):
            sql = 'SELECT id FROM users WHERE is_admin = 1'
            return [id for id, in c.execute(sql).fetchall()]

        return cls.transaction(func)

    @classmethod
    def is_registered(cls, id: int) -> bool:
        def func(c):
            sql = 'SELECT count(id) == 1 FROM users WHERE id = ?'
            params = (id,)
            return bool(c.execute(sql, params).fetchone()[0])

        return cls.transaction(func)

    @classmethod
    def is_admin(cls, id: int) -> bool:
        def func(c):
            sql = 'SELECT count(id) == 1 FROM users WHERE id = ? AND is_admin = 1'
            params = (id,)
            return bool(c.execute(sql, params).fetchone()[0])

        return cls.transaction(func)

    # @classmethod
    # def add_user(cls, id: int, owner_id: int) -> bool:
    #     def func(c):
    #         sql = 'INSERT INTO users (id, owner_id) VALUES (?, ?)'
    #         params = (id, owner_id)
    #         return bool(c.execute(sql, params).rowcount == 1)
    #
    #     return cls.transaction(func)

    @classmethod
    def add_user(cls, id: int) -> bool:
        def func(c):
            sql = 'SELECT owner_id FROM tokens ' \
                  'WHERE used_by = ? AND CURRENT_DATE < expire'
            params = (id,)
            owner_id = c.execute(sql, params).fetchone()[0]
            sql = 'INSERT INTO users (id, owner_id) VALUES (?, ?)'
            params = (id, owner_id)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)

    @classmethod
    def remove_user(cls, id: int) -> bool:
        def func(c):
            sql = 'DELETE FROM users WHERE id = ?'
            params = (id,)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)

    @classmethod
    def change_owner(cls, id: int, owner_id: int) -> bool:
        def func(c):
            sql = 'UPDATE users SET owner_id = ? WHERE id = ?'
            params = (owner_id, id)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)

    @classmethod
    def admin(cls, id: int, is_admin: bool) -> bool:
        def func(c):
            sql = 'UPDATE users SET is_admin = ? WHERE id = ?'
            params = (is_admin, id)
            return bool(c.execute(sql, params).rowcount == 1)

        return cls.transaction(func)
