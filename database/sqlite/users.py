from database.base_sqlite import BaseSqlite, transaction
from database.users_abstract import Users
from entities.user import User


class UsersSqlite(Users, BaseSqlite):
    @classmethod
    @transaction
    def create_table(cls, c):
        sql = 'CREATE TABLE IF NOT EXISTS users (' \
              'id INT PRIMARY KEY, ' \
              'is_admin INT DEFAULT 0, ' \
              'accounts_limit INT DEFAULT 1, ' \
              'owner_id INT DEFAULT NULL, ' \
              'language TEXT DEFAULT \'en\', ' \
              'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT)'
        c.execute(sql)
        sql = 'CREATE VIEW IF NOT EXISTS slaves AS ' \
              'WITH RECURSIVE slaves (leaf_id, id) AS (' \
              'SELECT id, id FROM users UNION ALL ' \
              'SELECT s.leaf_id, u.id FROM users u JOIN slaves s ON u.owner_id = s.id' \
              ') SELECT * FROM slaves'
        c.execute(sql)

    @classmethod
    @transaction
    def slaves(cls, id: int, c) -> list[int]:
        sql = 'SELECT id FROM slaves WHERE leaf_id = ?'
        params = (id,)
        return [_id for _id, in c.execute(sql, params).fetchall()]

    @classmethod
    @transaction
    def fetch_all(cls, c) -> list[User]:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users'
        return [User(id=id, is_admin=is_admin, accounts_limit=accounts_limit, language=language)
                for id, is_admin, accounts_limit, language in c.execute(sql).fetchall()]

    @classmethod
    @transaction
    def fetch(cls, id: int, c) -> User:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users WHERE id = ?'
        params = (id,)
        u = User()
        u.id, u.is_admin, u.accounts_limit, u.language = c.execute(sql, params).fetchone()
        return u

    @classmethod
    @transaction
    def add(cls, id: int, language: str, c) -> bool:
        sql = 'INSERT INTO users (id, owner_id, language) ' \
              'SELECT ?, t.owner_id, ? ' \
              'FROM tokens t INNER JOIN users u on u.id = t.owner_id ' \
              'WHERE t.used_by = ?'
        params = (id, language, id)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def remove_user(cls, id: int, c) -> bool:
        sql = 'DELETE FROM users WHERE id = ?'
        params = (id,)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def change_owner(cls, id: int, owner_id: int, c) -> bool:
        sql = 'UPDATE users SET owner_id = ? WHERE id = ?'
        params = (owner_id, id)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def admin(cls, id: int, is_admin: bool, c) -> bool:
        sql = 'UPDATE users SET is_admin = ? WHERE id = ?'
        params = (is_admin, id)
        return c.execute(sql, params).rowcount == 1
