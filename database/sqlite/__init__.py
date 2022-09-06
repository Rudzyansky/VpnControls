from .accounting import accounting
from .commands import commands
from .common import common
from .connection import ConnectionSqlite, connection
from .registration import registration


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
        'username TEXT NOT NULL UNIQUE COLLATE NOCASE, '
        'password TEXT NOT NULL); '

        'CREATE VIEW IF NOT EXISTS slaves AS '
        'WITH RECURSIVE slaves (leaf_id, id, tokens_limit) AS ('
        'SELECT owner_id, id, tokens_limit FROM users UNION ALL '
        'SELECT s.leaf_id, u.id, u.tokens_limit FROM users u JOIN slaves s ON u.owner_id = s.id '
        ') SELECT * FROM slaves; '

        'CREATE VIEW IF NOT EXISTS metrics AS '
        'SELECT u.id                                                    AS user_id, '
        '(SELECT COUNT(a.ROWID) FROM accounts a WHERE a.user_id = u.id) AS accounts, '
        '(SELECT COUNT(t.token) FROM tokens t WHERE t.owner_id = u.id)  AS tokens, '
        '(SELECT COUNT(t.token) > 0 FROM tokens t '
        '  WHERE t.owner_id = u.id '
        '    AND (t.used_by IS NULL OR t.used_by != t.owner_id) '
        '    AND CURRENT_DATE < expire)                                 AS has_actual_tokens, '
        '(SELECT COUNT(t.token) < u.tokens_limit FROM tokens t '
        '  WHERE t.owner_id = u.id)                                     AS can_issue_token, '
        '(SELECT COUNT(s.id) > 0 FROM slaves s WHERE u.id = s.leaf_id)  AS has_users '
        'FROM users u; '
    )


init()

__all__ = [
    'common',
    'registration',
    'commands',
    'accounting',
    'connection'
]
