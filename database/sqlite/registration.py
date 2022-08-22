from typing import Optional

from entities.token import Token
from entities.user import User
from . import ConnectionSqlite, connection
from ..abstract import Registration


class RegistrationSqlite(Registration):
    @classmethod
    @connection(False)
    def is_accept_invite(cls, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'SELECT COUNT(token) > 0 FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return bool(c.single(sql, user_id))

    @classmethod
    def add_user(cls, user: User, c: ConnectionSqlite = None) -> bool:
        sql = 'INSERT INTO users (id, is_admin, accounts_limit, owner_id, language, commands) ' \
              'SELECT ?, t.owner_id, ?, ?, ?, ? ' \
              'FROM tokens t INNER JOIN users u on u.id = t.owner_id ' \
              'WHERE t.used_by = ?'
        return c.update_one(sql, user.id, user.is_admin, user.accounts_limit, user.language, user.commands_int, user.id)

    @classmethod
    @connection()
    def revoke_token(cls, token: bytes, owner_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
        return c.update_one(sql, token, owner_id)

    @classmethod
    def revoke_token_by_user_id(cls, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id WHERE used_by = ? AND CURRENT_DATE < expire'
        return c.update_one(sql, user_id)

    @classmethod
    def free_token_by_user_id(cls, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE tokens SET used_by = NULL WHERE used_by = ? AND CURRENT_DATE < expire'
        return c.update_one(sql, user_id)

    @classmethod
    def use_token(cls, token: bytes, owner_id: int, user_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'UPDATE tokens SET used_by = ? ' \
              'WHERE token = ? AND owner_id = ? AND used_by IS NULL AND CURRENT_DATE < expire'
        return c.update_one(sql, user_id, token, owner_id)

    @classmethod
    def add_token(cls, token: bytes, owner_id: int, c: ConnectionSqlite = None) -> bool:
        sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
              'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
        return c.update_one(sql, token, owner_id)

    @classmethod
    @connection(False)
    def get_token(cls, token: bytes, owner_id: int, c: ConnectionSqlite = None) -> Optional[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        result = c.fetch_one(sql, token, owner_id)
        if result is None:
            return None
        token, expire, used_by = result
        return Token(data=token, expire=expire, used_by=used_by)

    @classmethod
    @connection(False)
    def get_all_tokens(cls, owner_id: int, c: ConnectionSqlite = None) -> list[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? AND CURRENT_DATE < expire'
        return [Token(data=token, expire=expire, used_by=used_by)
                for token, expire, used_by in c.fetch_all(sql, owner_id)]

    @classmethod
    @connection(False)
    def get_actual_tokens(cls, owner_id: int, c: ConnectionSqlite = None) -> list[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? ' \
              'AND (used_by IS NULL OR used_by != owner_id) AND CURRENT_DATE < expire'
        return [Token(data=token, expire=expire, used_by=used_by)
                for token, expire, used_by in c.fetch_all(sql, owner_id)]


registration: Registration = RegistrationSqlite()
