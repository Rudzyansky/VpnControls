from .connection import ConnectionSqlite
from ..abstract.privileges import Privileges


class PrivilegesSqlite(Privileges):
    @classmethod
    def get_users_page(cls, owner_id: int, offset: int, count: int, c: ConnectionSqlite = None) -> list[int]:
        sql = 'SELECT id FROM users WHERE owner_id = ? ORDER BY registration_time LIMIT ?, ?'
        return [id for id, in c.fetch_all(sql, owner_id, offset, count)]

    @classmethod
    def get_users_count(cls, owner_id: int, c: ConnectionSqlite = None) -> int:
        sql = 'SELECT COUNT(id) FROM users WHERE owner_id = ? ORDER BY registration_time LIMIT ?, ?'
        return int(c.single(sql, owner_id))


privileges: Privileges = PrivilegesSqlite()
