from .commands import commands
from .common import common
from .connection import ConnectionSqlite, connection
from .registration import registration
from .accounting import accounting


@connection()
def init(c: ConnectionSqlite):
    c.data.executescript(
        'CREATE TABLE IF NOT EXISTS users ('
        'id INT PRIMARY KEY, '
        'tokens_limit INT NOT NULL, '
        'accounts_limit INT NOT NULL, '
        'owner_id INT DEFAULT NULL, '
        'language TEXT NOT NULL, '
        'commands INT NOT NULL, '
        'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT); '

        'CREATE TABLE IF NOT EXISTS tokens ('
        'token BLOB NOT NULL , '
        'owner_id INT NOT NULL, '
        'expire BLOB NOT NULL, '
        'used_by INT DEFAULT NULL, '
        'PRIMARY KEY (token, owner_id), '
        'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT); '

        'CREATE TABLE IF NOT EXISTS accounts ('
        'user_id INT NOT NULL, '
        'position INT NOT NULL, '
        'FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE RESTRICT ON UPDATE RESTRICT); '

        'CREATE VIEW IF NOT EXISTS slaves AS '
        'WITH RECURSIVE slaves (leaf_id, id, tokens_limit) AS ('
        'SELECT owner_id, id, tokens_limit FROM users UNION ALL '
        'SELECT s.leaf_id, u.id, u.tokens_limit FROM users u JOIN slaves s ON u.owner_id = s.id '
        ') SELECT * FROM slaves; '

        'CREATE VIEW IF NOT EXISTS metrics AS '
        'SELECT u.id                                                                  AS user_id, '
        'COUNT(a.ROWID)                                                               AS accounts, '
        'COUNT(t.token)                                                               AS tokens, '
        '(SELECT COUNT(t.token) > 0 WHERE CURRENT_DATE < t.expire)                    AS has_actual_tokens, '
        'COUNT(t.token) < u.tokens_limit                                              AS can_issue_token, '
        'COUNT(s.id) > 0                                                              AS has_users '
        'FROM users u '
        'LEFT JOIN accounts a ON u.id = a.user_id '
        'LEFT JOIN tokens t ON u.id = t.owner_id '
        'LEFT JOIN slaves s ON u.id = s.leaf_id; '
    )


init()

__all__ = [
    'common',
    'registration',
    'commands',
    'accounting',
    'connection'
]
