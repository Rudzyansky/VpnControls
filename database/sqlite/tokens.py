from typing import Optional

from database.base_sqlite import BaseSqlite, transaction
from database.tokens_abstract import Tokens
from entities.token import Token


class TokensSqlite(Tokens, BaseSqlite):
    @classmethod
    @transaction
    def create_table(cls, c):
        sql = 'CREATE TABLE IF NOT EXISTS tokens (' \
              'token BLOB NOT NULL , ' \
              'owner_id INT NOT NULL, ' \
              'expire BLOB NOT NULL, ' \
              'used_by INT DEFAULT NULL, ' \
              'PRIMARY KEY (token), ' \
              'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT)'
        c.execute(sql)

    @classmethod
    @transaction
    def add(cls, token: Token, c) -> Optional[Token]:
        sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
              'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
        params = (token.bytes, token.owner_id)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def fetch(cls, token: Token, c) -> Optional[Token]:
        sql = 'SELECT expire, used_by FROM tokens ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        params = (token.bytes, token.owner_id)
        result = c.execute(sql, params).fetchone()
        if result is None:
            return None
        token.expire, token.used_by = result
        return token

    @classmethod
    @transaction
    def get_all(cls, owner_id: int, c) -> list:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? AND CURRENT_DATE < expire'
        params = (owner_id,)
        return [Token(data=token, expire=expire, used_by=used_by)
                for token, expire, used_by in c.execute(sql, params).fetchall()]

    @classmethod
    @transaction
    def use(cls, token: Token, c) -> bool:
        sql = 'UPDATE tokens SET used_by = NULL WHERE used_by = ? AND CURRENT_DATE < expire'
        params = (token.used_by,)
        c.execute(sql, params)

        sql = 'UPDATE tokens SET used_by = ? ' \
              'WHERE token = ? AND owner_id = ? AND used_by IS NULL AND CURRENT_DATE < expire'
        params = (token.used_by, token.bytes, token.owner_id)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def revoke(cls, token: Token, c) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
        params = (token.bytes, token.owner_id)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def revoke_by_used(cls, user_id: int, c) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id WHERE used_by = ? AND CURRENT_DATE < expire'
        params = (user_id,)
        return c.execute(sql, params).rowcount == 1

    @classmethod
    @transaction
    def is_accept_invite(cls, user_id: int, c) -> bool:
        sql = 'SELECT COUNT(token) > 0 FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        params = (user_id,)
        return bool(c.execute(sql, params).fetchone()[0])

    @classmethod
    @transaction
    def get_owner(cls, user_id: int, c) -> Optional[int]:
        sql = 'SELECT owner_id FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        params = (user_id,)
        return c.execute(sql, params).fetchone()[0]

    @classmethod
    @transaction
    def remove_expired(cls, c) -> bool:
        sql = 'DELETE FROM tokens WHERE CURRENT_DATE >= expire'
        return bool(c.execute(sql).rowcount > 0)
