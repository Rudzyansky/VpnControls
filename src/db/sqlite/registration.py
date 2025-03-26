from typing import Optional, List

from db.abstract import RegistrationRepositoryAbstract
from db.sqlite.base import SQLiteBase
from entities.token import Token
from entities.user import User


class RegistrationRepositorySQLite(SQLiteBase, RegistrationRepositoryAbstract):
    def is_accept_invite(self, user_id: int) -> bool:
        sql = 'SELECT COUNT(token) > 0 FROM tokens WHERE used_by = ? AND CURRENT_DATE < expire'
        return bool(self.query(sql, (user_id,), output='scalar'))

    def add_user(self, user: User) -> bool:
        sql = 'INSERT INTO users (id, tokens_limit, accounts_limit, owner_id, language, commands, registration_time) ' \
              'SELECT ?, ?, ?, t.owner_id, ?, ?, CURRENT_TIMESTAMP ' \
              'FROM tokens t INNER JOIN users u on u.id = t.owner_id ' \
              'WHERE t.used_by = ?'
        return self.query(sql, (user.id, user.tokens_limit, user.accounts_limit,
                                user.language, user.commands_int, user.id), output='rowcount') == 1

    def revoke_token(self, token: bytes, owner_id: int) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire'
        return self.query(sql, (token, owner_id), output='rowcount') == 1

    def revoke_token_by_user_id(self, user_id: int) -> bool:
        sql = 'UPDATE tokens SET used_by = owner_id WHERE used_by = ? AND CURRENT_DATE < expire'
        return self.query(sql, (user_id,), output='rowcount') == 1

    def free_token_by_user_id(self, user_id: int) -> bool:
        sql = 'UPDATE tokens SET used_by = NULL WHERE used_by = ? AND CURRENT_DATE < expire'
        return self.query(sql, (user_id,), output='rowcount') == 1

    def use_token(self, token: bytes, owner_id: int, user_id: int) -> bool:
        sql = 'UPDATE tokens SET used_by = ? ' \
              'WHERE token = ? AND owner_id = ? ' \
              'AND (used_by IS NULL OR used_by = ?) ' \
              'AND CURRENT_DATE < expire'
        return self.query(sql, (user_id, token, owner_id, user_id), output='rowcount') == 1

    def add_token(self, token: bytes, owner_id: int) -> bool:
        sql = 'INSERT INTO tokens (token, owner_id, expire) ' \
              'VALUES (?, ?, DATE(CURRENT_DATE, \'+8 days\'))'
        return self.query(sql, (token, owner_id), output='rowcount') == 1

    def get_token(self, token: bytes) -> Optional[Token]:
        sql = 'SELECT token, expire, used_by, owner_id FROM tokens ' \
              'WHERE token = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        result = self.query(sql, (token,), output='fetchone')
        if result is None:
            return None
        token, expire, used_by, owner_id = result
        return Token(data=token, expire=expire, used_by=used_by, owner_id=owner_id)

    def fetch_token(self, token: bytes, owner_id: int) -> Optional[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens ' \
              'WHERE token = ? AND owner_id = ? AND CURRENT_DATE < expire ' \
              'AND (used_by NOT LIKE owner_id OR used_by IS NULL)'
        result = self.query(sql, (token, owner_id), output='fetchone')
        if result is None:
            return None
        token, expire, used_by = result
        return Token(data=token, expire=expire, used_by=used_by, owner_id=owner_id)

    def get_all_tokens(self, owner_id: int) -> List[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? AND CURRENT_DATE < expire'
        results = self.query(sql, (owner_id,), output='fetchall')
        return [Token(data=token, expire=expire, used_by=used_by, owner_id=owner_id)
                for token, expire, used_by in results]

    def get_actual_tokens(self, owner_id: int) -> List[Token]:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? ' \
              'AND (used_by IS NULL OR used_by != owner_id) AND CURRENT_DATE < expire'
        results = self.query(sql, (owner_id,), output='fetchall')
        return [Token(data=token, expire=expire, used_by=used_by, owner_id=owner_id)
                for token, expire, used_by in results]

    def count_of_tokens(self, owner_id: int) -> int:
        return int(self.query('SELECT COUNT(token) FROM tokens WHERE owner_id = ? '
                              'AND CURRENT_DATE < expire', (owner_id,), output='scalar'))

    def get_tokens_limit(self, user_id: int) -> int:
        return int(self.query('SELECT tokens_limit FROM users WHERE id = ?', (user_id,), output='scalar'))

    def get_next_actual_token(self, owner_id: int, offset: int) -> Token:
        sql = 'SELECT token, expire, used_by FROM tokens WHERE owner_id = ? ' \
              'AND (used_by IS NULL OR used_by != owner_id) AND CURRENT_DATE < expire LIMIT ?, 1'
        result = self.query(sql, (owner_id, offset), output='fetchone')
        token, expire, used_by = result
        return Token(data=token, expire=expire, used_by=used_by, owner_id=owner_id)

    def count_of_actual_tokens(self, owner_id: int) -> int:
        sql = 'SELECT COUNT(token) FROM tokens WHERE owner_id = ? ' \
              'AND (used_by IS NULL OR used_by != owner_id) AND CURRENT_DATE < expire'
        return self.query(sql, (owner_id,), output='scalar')


registration: RegistrationRepositoryAbstract = RegistrationRepositorySQLite()
