from typing import Optional

from database.abstract import Tokens
from entities.token import Token
from .connection import ConnectionSqlite, connection


class TokensSqlite(Tokens):
    @classmethod
    @connection
    def add(cls, token: Token, c: ConnectionSqlite) -> Optional[Token]:
        sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
              'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
        return c.update_one(sql, token.bytes, token.owner_id)

    @classmethod
    @connection(False)
    def fetch(cls, token: Token, c: ConnectionSqlite) -> Optional[Token]:
        sql = 'SELECT expire, used_by FROM tokens ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        result = c.fetch_one(sql, token.bytes, token.owner_id)
        if result is None:
            return None
        token.expire, token.used_by = result
        return token

    @classmethod
    @connection(False)
    def get_all(cls, owner_id: int, c: ConnectionSqlite) -> list:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? AND CURRENT_DATE < expire'
        return [Token(data=token, expire=expire, used_by=used_by)
                for token, expire, used_by in c.fetch_all(sql, owner_id)]

    @classmethod
    @connection
    def use(cls, token: Token, c: ConnectionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = NULL WHERE used_by = ? AND CURRENT_DATE < expire'
        c.execute(sql, token.used_by)

        sql = 'UPDATE tokens SET used_by = ? ' \
              'WHERE token = ? AND owner_id = ? AND used_by IS NULL AND CURRENT_DATE < expire'
        return c.update_one(sql, token.used_by, token.bytes, token.owner_id)

    @classmethod
    @connection
    def revoke(cls, token: Token, c: ConnectionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
        return c.update_one(sql, token.bytes, token.owner_id)

    @classmethod
    @connection
    def revoke_by_used(cls, user_id: int, c: ConnectionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id WHERE used_by = ? AND CURRENT_DATE < expire'
        return c.update_one(sql, user_id)

    @classmethod
    @connection(False)
    def is_accept_invite(cls, user_id: int, c: ConnectionSqlite) -> bool:
        sql = 'SELECT COUNT(token) > 0 FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return bool(c.single(sql, user_id))

    @classmethod
    @connection(False)
    def get_owner(cls, user_id: int, c: ConnectionSqlite) -> Optional[int]:
        sql = 'SELECT owner_id FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return c.single(sql, user_id)

    @classmethod
    @connection
    def remove_expired(cls, c: ConnectionSqlite) -> bool:
        return c.update_many('DELETE FROM tokens WHERE CURRENT_DATE >= expire')
