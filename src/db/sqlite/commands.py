from db.abstract import CommandsRepositoryAbstract
from db.sqlite.base import SQLiteBase


class CommandsRepositorySQLite(SQLiteBase, CommandsRepositoryAbstract):
    def recalculate_commands(self, user_id: int = None):
        sql = ('UPDATE users SET commands = (SELECT '
               '((accounts < accounts_limit) <<  1) | '  # CAN_CREATE_ACCOUNT
               '((accounts > 0)              <<  2) | '  # HAS_ACCOUNTS
               '( can_issue_token            <<  3) | '  # CAN_ISSUE_TOKEN
               '( has_actual_tokens          <<  4) | '  # HAS_ACTUAL_TOKENS
               '((tokens > 0)                <<  5) | '  # HAS_TOKENS
               '( has_users                  <<  6) | '  # HAS_USERS
               '( 1                          <<  0)   '  # REGISTERED
               'FROM metrics WHERE user_id = users.id) ')
        if user_id is None:
            self.query(sql, output='rowcount')
        else:
            self.query(sql + 'WHERE u.id = ?', (user_id,), output='rowcount')

    def set_user_commands(self, user_id: int, categories: int) -> bool:
        return self.query('UPDATE users SET commands = ? WHERE id = ?', (categories, user_id), output='rowcount') == 1


commands: CommandsRepositoryAbstract = CommandsRepositorySQLite()
