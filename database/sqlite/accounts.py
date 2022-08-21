from database.accounts_abstract import Accounts


class AccountsSqlite(Accounts):
    @classmethod
    @transaction
    def remove_username(cls, id: int, c) -> bool:
        sql = 'DELETE FROM accounts WHERE id = ? AND username = ?'
        params = (id, username)
        return bool(c.execute(sql, params).rowcount == 1)

    @classmethod
    @transaction
    def change_username(cls, id: int, new_username: str, c) -> bool:
        sql = 'UPDATE users SET username = ? WHERE id = ?'
        params = (new_username, id)
        return bool(c.execute(sql, params).rowcount == 1)

    @classmethod
    @transaction
    def change_pos(cls, *set: tuple[int, int], c) -> bool:
        sql = 'UPDATE users SET pos = ? WHERE id = ?'
        params = set
        return bool(c.executemany(sql, params).rowcount == len(set))
