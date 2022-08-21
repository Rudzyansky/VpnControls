from database.abstract import Users
from entities.user import User
from .connection import ConnectionSqlite, connection


class UsersSqlite(Users):
    @classmethod
    @connection(False)
    def slaves(cls, id: int, c: ConnectionSqlite) -> list[int]:
        return [i for i, in c.fetch_all('SELECT id FROM slaves WHERE leaf_id = ?', id)]

    @classmethod
    @connection(False)
    def fetch_all(cls, c: ConnectionSqlite) -> list[User]:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users'
        return [User(id=id, is_admin=is_admin, accounts_limit=accounts_limit, language=language)
                for id, is_admin, accounts_limit, language in c.fetch_all(sql)]

    @classmethod
    @connection(False)
    def fetch(cls, id: int, c: ConnectionSqlite) -> User:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users WHERE id = ?'
        id, is_admin, accounts_limit, language = c.fetch_one(sql, id)
        return User(id=id, is_admin=is_admin, accounts_limit=accounts_limit, language=language)

    @classmethod
    @connection
    def add(cls, id: int, language: str, c: ConnectionSqlite) -> bool:
        sql = 'INSERT INTO users (id, owner_id, language) ' \
              'SELECT ?, t.owner_id, ? ' \
              'FROM tokens t INNER JOIN users u on u.id = t.owner_id ' \
              'WHERE t.used_by = ?'
        return c.update_one(sql, id, language, id)

    @classmethod
    @connection
    def remove_user(cls, id: int, c: ConnectionSqlite) -> bool:
        return c.update_one('DELETE FROM users WHERE id = ?', id)

    @classmethod
    @connection
    def change_owner(cls, id: int, owner_id: int, c: ConnectionSqlite) -> bool:
        return c.update_one('UPDATE users SET owner_id = ? WHERE id = ?', owner_id, id)

    @classmethod
    @connection
    def admin(cls, id: int, is_admin: bool, c: ConnectionSqlite) -> bool:
        return c.update_one('UPDATE users SET is_admin = ? WHERE id = ?', is_admin, id)
