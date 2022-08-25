from typing import Optional

from entities.user import User
from .connection import ConnectionSqlite, connection
from ..abstract import Common


class CommonSqlite(Common):
    @classmethod
    @connection(False)
    def get_all_users(cls, c: ConnectionSqlite = None) -> list[User]:
        sql = 'SELECT id, tokens_limit, accounts_limit, language, commands FROM users'
        return [User(id=id, tokens_limit=tokens_limit, accounts_limit=accounts_limit,
                     language=language, _commands=commands)
                for id, tokens_limit, accounts_limit, language, commands in c.fetch_all(sql)]

    @classmethod
    def get_user(cls, user_id: int, c: ConnectionSqlite = None) -> Optional[User]:
        sql = 'SELECT id, tokens_limit, accounts_limit, language, commands FROM users WHERE id = ?'
        id, tokens_limit, accounts_limit, language, commands = c.fetch_one(sql, user_id)
        return User(id=id, tokens_limit=tokens_limit, accounts_limit=accounts_limit,
                    language=language, _commands=commands)

    @classmethod
    def remove_expired_tokens(cls, c: ConnectionSqlite = None) -> bool:
        return c.update_many('DELETE FROM tokens WHERE CURRENT_DATE >= expire')


common: Common = CommonSqlite()
