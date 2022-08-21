from database.abstract import Users
from entities.user import User
from .transaction import TransactionSqlite, transaction


class UsersSqlite(Users):
    @classmethod
    @transaction
    def slaves(cls, id: int, t: TransactionSqlite) -> list[int]:
        return [i for i, in t.fetch_all('SELECT id FROM slaves WHERE leaf_id = ?', id)]

    @classmethod
    @transaction
    def fetch_all(cls, t: TransactionSqlite) -> list[User]:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users'
        return [User(id=id, is_admin=is_admin, accounts_limit=accounts_limit, language=language)
                for id, is_admin, accounts_limit, language in t.fetch_all(sql)]

    @classmethod
    @transaction
    def fetch(cls, id: int, t: TransactionSqlite) -> User:
        sql = 'SELECT id, is_admin, accounts_limit, language FROM users WHERE id = ?'
        id, is_admin, accounts_limit, language = t.fetch_one(sql, id)
        return User(id=id, is_admin=is_admin, accounts_limit=accounts_limit, language=language)

    @classmethod
    @transaction
    def add(cls, id: int, language: str, t: TransactionSqlite) -> bool:
        sql = 'INSERT INTO users (id, owner_id, language) ' \
              'SELECT ?, t.owner_id, ? ' \
              'FROM tokens t INNER JOIN users u on u.id = t.owner_id ' \
              'WHERE t.used_by = ?'
        return t.update_one(sql, id, language, id)

    @classmethod
    @transaction
    def remove_user(cls, id: int, t: TransactionSqlite) -> bool:
        return t.update_one('DELETE FROM users WHERE id = ?', id)

    @classmethod
    @transaction
    def change_owner(cls, id: int, owner_id: int, t: TransactionSqlite) -> bool:
        return t.update_one('UPDATE users SET owner_id = ? WHERE id = ?', owner_id, id)

    @classmethod
    @transaction
    def admin(cls, id: int, is_admin: bool, t: TransactionSqlite) -> bool:
        return t.update_one('UPDATE users SET is_admin = ? WHERE id = ?', is_admin, id)
