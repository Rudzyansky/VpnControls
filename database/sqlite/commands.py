from .connection import ConnectionSqlite, connection
from .. import Commands


class CommandsSqlite(Commands):
    @classmethod
    @connection()
    def recalculate_commands(cls, user_id: int = None, c: ConnectionSqlite = None):
        sql = ('UPDATE users SET commands = (SELECT '
               '((accounts == 0)    <<  0) | '  # NO_ACCOUNTS
               '((accounts == 1)    <<  1) | '  # ONE_ACCOUNT
               '((accounts > 1)     <<  2) | '  # MANY_ACCOUNTS
               '((tokens == 0)      <<  3) | '  # NO_TOKENS
               '( has_actual_tokens <<  4) | '  # HAS_ACTUAL_TOKENS
               '( can_issue_token   <<  5) | '  # CAN_ISSUE_TOKEN
               '((tokens > 0)       <<  6) | '  # HAS_TOKENS
               '( has_slaves        <<  7) | '  # HAS_SLAVES
               '( has_slaves        <<  8) | '  # GRANT
               # '( has_slaves_admins <<  9) | '  # HAS_INVITED
               '( 1                 << 10)   '  # COMMON
               'FROM metrics WHERE users.id == metrics.user_id) ')
        if user_id is None:
            c.update_many(sql)
        else:
            c.update_one(sql + 'WHERE u.id = ?', user_id)

    @classmethod
    @connection()
    def set_user_commands(cls, user_id: int, categories: int, c: ConnectionSqlite = None) -> bool:
        return c.update_one('UPDATE users SET commands = ? WHERE id = ?', categories, user_id)


commands: Commands = CommandsSqlite()
