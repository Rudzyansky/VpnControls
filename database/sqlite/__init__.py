from .common import CommonSqlite
from .connection import ConnectionSqlite, connection
from .registration import RegistrationSqlite


@connection()
def init(c: ConnectionSqlite):
    c.data.executescript(
        'CREATE TABLE IF NOT EXISTS users ('
        'id INT PRIMARY KEY, '
        'is_admin INT DEFAULT 0, '
        'accounts_limit INT DEFAULT 1, '
        'owner_id INT DEFAULT NULL, '
        'language TEXT DEFAULT \'en\', '
        'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT); '

        # SELECT id FROM slaves WHERE leaf_id = ?', id
        'CREATE VIEW IF NOT EXISTS slaves AS '
        'WITH RECURSIVE slaves (leaf_id, id) AS ('
        'SELECT id, id FROM users UNION ALL '
        'SELECT s.leaf_id, u.id FROM users u JOIN slaves s ON u.owner_id = s.id'
        ') SELECT * FROM slaves; '

        'CREATE TABLE IF NOT EXISTS tokens ('
        'token BLOB NOT NULL , '
        'owner_id INT NOT NULL, '
        'expire BLOB NOT NULL, '
        'used_by INT DEFAULT NULL, '
        'PRIMARY KEY (token), '
        'FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT); '

        'CREATE TABLE IF NOT EXISTS accounts ('
        'id INT not null, '
        'username TEXT not null, '
        'pos INT not null unique, '
        'PRIMARY KEY (id, username), '
        'FOREIGN KEY (id) REFERENCES users (id) on delete RESTRICT on update RESTRICT); '
    )


__all__ = [
    'CommonSqlite',
    'RegistrationSqlite',
    'connection',
    'init'
]
