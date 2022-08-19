from typing import Optional

from database.base_sqlite import BaseSqlite
from database.tokens_abstract import Tokens
from handlers.token import Token


class TokensSqlite(Tokens, BaseSqlite):
    @classmethod
    def create_table(cls):
        def func(c):
            sql = 'CREATE TABLE IF NOT EXISTS tokens (' \
                  'token BLOB NOT NULL , ' \
                  'owner_id INT NOT NULL, ' \
                  'expire BLOB NOT NULL, ' \
                  'used_by INT DEFAULT NULL, ' \
                  'PRIMARY KEY (token), ' \
                  'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT)'
            c.execute(sql)

        cls.transaction(func)

    @classmethod
    def add(cls, token: Token) -> Optional[Token]:
        def func(c):
            sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
                  'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
            params = (token.bytes, token.owner_id)
            if not c.execute(sql, params).rowcount == 1:
                return None
            sql = 'SELECT expire FROM tokens WHERE token = ?'
            params = (token.bytes,)
            result = c.execute(sql, params).fetchone()
            if result is None:
                return None
            token.expire, = result
            return token

        return cls.transaction(func)

    @classmethod
    def get(cls, token: Token) -> list:
        def func(c):
            sql = 'SELECT expire, used_by FROM tokens ' \
                  'WHERE token = ? ' \
                  'AND owner_id = ? ' \
                  'AND (used_by NOT LIKE owner_id OR used_by IS NULL) ' \
                  'AND CURRENT_DATE < expire'
            params = (token.bytes, token.owner_id)
            result = c.execute(sql, params).fetchone()
            if result is None:
                return None
            token.expire, token.used_by = result
            return token

        return cls.transaction(func)

    @classmethod
    def get_all(cls, owner_id: int) -> list:
        def func(c):
            sql = 'SELECT token, expire, used_by FROM tokens ' \
                  'WHERE owner_id = ? ' \
                  'AND CURRENT_DATE < expire'
            params = (owner_id,)
            return [Token(t, e, u, owner_id) for t, e, u in c.execute(sql, params).fetchall()]

        return cls.transaction(func)

    @classmethod
    def use(cls, token: Token) -> bool:
        def func(c):
            sql = 'UPDATE tokens SET used_by = ? ' \
                  'WHERE token = ? AND owner_id = ? AND used_by IS NULL AND CURRENT_DATE < expire'
            params = (token.used_by, token.bytes, token.owner_id)
            return c.execute(sql, params).rowcount == 1

        return cls.transaction(func)

    @classmethod
    def revoke(cls, token: Token) -> bool:
        def func(c):
            sql = 'UPDATE tokens SET used_by = owner_id ' \
                  'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
            params = (token.bytes, token.owner_id)
            return c.execute(sql, params).rowcount == 1

        return cls.transaction(func)

    @classmethod
    def check_user(cls, user_id: int) -> bool:
        def func(c):
            sql = 'SELECT COUNT(token) > 0 FROM tokens ' \
                  'WHERE used_by = ? AND CURRENT_DATE < expire'
            params = (user_id,)
            return bool(c.execute(sql, params).fetchone()[0])

        return cls.transaction(func)

    @classmethod
    def get_owner(cls, user_id: int) -> Optional[int]:
        def func(c):
            sql = 'SELECT owner_id FROM tokens ' \
                  'WHERE used_by = ? AND CURRENT_DATE < expire'
            params = (user_id,)
            return c.execute(sql, params).fetchone()[0]

        return cls.transaction(func)

    @classmethod
    def remove_expired(cls) -> bool:
        def func(c):
            sql = 'DELETE FROM tokens WHERE CURRENT_DATE >= expire'
            return bool(c.execute(sql).rowcount > 0)

        return cls.transaction(func)
