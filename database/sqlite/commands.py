from .connection import ConnectionSqlite, connection
from .. import Commands


class CommandsSqlite(Commands):
    @classmethod
    @connection()
    def recalculate_commands(cls, user_id: int = None, c: ConnectionSqlite = None):
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
            c.update_many(sql)
        else:
            c.update_one(sql + 'WHERE u.id = ?', user_id)

    @classmethod
    @connection()
    def set_user_commands(cls, user_id: int, categories: int, c: ConnectionSqlite = None) -> bool:
        return c.update_one('UPDATE users SET commands = ? WHERE id = ?', categories, user_id)


commands: Commands = CommandsSqlite()
