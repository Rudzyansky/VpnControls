from typing import Optional

from database.abstract import Tokens
from entities.token import Token
from .transaction import TransactionSqlite, transaction


class TokensSqlite(Tokens):
    @classmethod
    @transaction
    def add(cls, token: Token, t: TransactionSqlite) -> Optional[Token]:
        sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
              'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
        return t.update_one(sql, token.bytes, token.owner_id)

    @classmethod
    @transaction
    def fetch(cls, token: Token, t: TransactionSqlite) -> Optional[Token]:
        sql = 'SELECT expire, used_by FROM tokens ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        result = t.fetch_one(sql, token.bytes, token.owner_id)
        if result is None:
            return None
        token.expire, token.used_by = result
        return token

    @classmethod
    @transaction
    def get_all(cls, owner_id: int, t: TransactionSqlite) -> list:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? AND CURRENT_DATE < expire'
        return [Token(data=token, expire=expire, used_by=used_by)
                for token, expire, used_by in t.fetch_all(sql, owner_id)]

    @classmethod
    @transaction
    def use(cls, token: Token, t: TransactionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = NULL WHERE used_by = ? AND CURRENT_DATE < expire'
        t.execute(sql, token.used_by)

        sql = 'UPDATE tokens SET used_by = ? ' \
              'WHERE token = ? AND owner_id = ? AND used_by IS NULL AND CURRENT_DATE < expire'
        return t.update_one(sql, token.used_by, token.bytes, token.owner_id)

    @classmethod
    @transaction
    def revoke(cls, token: Token, t: TransactionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
        return t.update_one(sql, token.bytes, token.owner_id)

    @classmethod
    @transaction
    def revoke_by_used(cls, user_id: int, t: TransactionSqlite) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id WHERE used_by = ? AND CURRENT_DATE < expire'
        return t.update_one(sql, user_id)

    @classmethod
    @transaction
    def is_accept_invite(cls, user_id: int, t: TransactionSqlite) -> bool:
        sql = 'SELECT COUNT(token) > 0 FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return bool(t.single(sql, user_id))

    @classmethod
    @transaction
    def get_owner(cls, user_id: int, t: TransactionSqlite) -> Optional[int]:
        sql = 'SELECT owner_id FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return t.single(sql, user_id)

    @classmethod
    @transaction
    def remove_expired(cls, t: TransactionSqlite) -> bool:
        return t.update_many('DELETE FROM tokens WHERE CURRENT_DATE >= expire')
