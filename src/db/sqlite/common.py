from typing import Optional, List

from db.abstract import CommonRepositoryAbstract
from db.sqlite.base import SQLiteBase
from entities.user import User


class CommonRepositorySQLite(SQLiteBase, CommonRepositoryAbstract):
    def get_all_users(self) -> List[User]:
        sql = 'SELECT id, tokens_limit, accounts_limit, language, commands FROM users'
        results = self.query(sql, output='fetchall')
        return [User(id=user_id, tokens_limit=tokens_limit, accounts_limit=accounts_limit,
                     language=language, _commands=commands)
                for user_id, tokens_limit, accounts_limit, language, commands in results]

    def get_user(self, user_id: int) -> Optional[User]:
        sql = 'SELECT id, tokens_limit, accounts_limit, language, commands FROM users WHERE id = ?'
        result = self.query(sql, (user_id,), output='fetchone')
        if result is None:
            return None
        user_id, tokens_limit, accounts_limit, language, commands = result
        return User(id=user_id, tokens_limit=tokens_limit, accounts_limit=accounts_limit,
                    language=language, _commands=commands)

    def set_language(self, user_id: int, lang_code: str) -> bool:
        return self.query('UPDATE users SET language = ? WHERE id = ?', (lang_code, user_id), output='rowcount') == 1

    def remove_expired_tokens(self) -> bool:
        return self.query('DELETE FROM tokens WHERE CURRENT_DATE >= expire', output='rowcount') > 0


common: CommonRepositoryAbstract = CommonRepositorySQLite()
