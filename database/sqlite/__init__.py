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
        'username TEXT NOT NULL, '
        'pos INT NOT NULL, '
        'PRIMARY KEY (user_id, username), '
        'FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE RESTRICT ON UPDATE RESTRICT); '

        # SELECT id FROM slaves WHERE leaf_id = ?
        'CREATE VIEW IF NOT EXISTS slaves AS '
        'WITH RECURSIVE slaves (leaf_id, id, tokens_limit) AS ('
        'SELECT owner_id, id, tokens_limit FROM users UNION ALL '
        'SELECT s.leaf_id, u.id, u.tokens_limit FROM users u JOIN slaves s ON u.owner_id = s.id '
        ') SELECT * FROM slaves; '
    )


init()

__all__ = [
    'common',
    'registration',
    'connection'
]
