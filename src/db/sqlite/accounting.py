from typing import Optional, List

from db.sqlite.base import SQLiteBase
from entities.account import Account
from ..abstract.accounting import AccountingRepositoryAbstract


class AccountingRepositorySQLite(SQLiteBase, AccountingRepositoryAbstract):
    def get_users(self) -> List[int]:
        sql = 'SELECT DISTINCT user_id FROM accounts'
        results = self.query(sql, output='fetchall')
        return [user_id for user_id, in results]

    def get_accounts(self, user_id: int) -> List[Account]:
        sql = 'SELECT ROWID, username, password FROM accounts WHERE user_id = ?'
        results = self.query(sql, (user_id,), output='fetchall')
        return [Account(id=r[0], username=r[1], password=r[2]) for r in results]

    def get_account_position(self, user_id: int, account_id: int) -> Optional[int]:
        sql = 'SELECT position FROM accounts WHERE ROWID = ? AND user_id = ?'
        return int(self.query(sql, (account_id, user_id), output='scalar'))

    def get_account(self, user_id: int, account_id: int) -> Optional[Account]:
        sql = 'SELECT ROWID, username, password FROM accounts WHERE ROWID = ? AND user_id = ?'
        r = self.query(sql, (account_id, user_id), output='fetchone')
        return None if r is None else Account(id=r[0], username=r[1], password=r[2])

    def get_account_by_offset(self, user_id: int, offset: int) -> Optional[Account]:
        sql = 'SELECT ROWID, username, password FROM accounts WHERE user_id = ? ORDER BY position LIMIT ?, 1'
        r = self.query(sql, (user_id, offset), output='fetchone')
        return None if r is None else Account(id=r[0], username=r[1], password=r[2])

    def is_username_exist(self, username: str) -> bool:
        return bool(
            self.query('SELECT COUNT(ROWID) > 0 FROM accounts WHERE username = ?', (username,), output='scalar'))

    def add_account(self, user_id: int, position: int, username: str, password: str) -> int:
        sql = 'INSERT INTO accounts (user_id, position, username, password) VALUES (?, ?, ?, ?)'
        return self.query(sql, (user_id, position, username, password), output='lastrowid')

    def set_username(self, user_id: int, account_id: int, username: str) -> bool:
        sql = 'UPDATE accounts SET username = ? WHERE user_id = ? AND ROWID = ?'
        return self.query(sql, (username, user_id, account_id), output='rowcount') == 1

    def set_password(self, user_id: int, account_id: int, password: str) -> bool:
        sql = 'UPDATE accounts SET password = ? WHERE user_id = ? AND ROWID = ?'
        return self.query(sql, (password, user_id, account_id), output='rowcount') == 1

    def set_position(self, account_id: int, position: int) -> bool:
        return self.query('UPDATE accounts SET position = ? WHERE ROWID = ?', (position, account_id),
                          output='rowcount') == 1

    def move_accounts(self, user_id: int, position: int, diff: int) -> bool:
        sql = 'UPDATE accounts SET position = position + ? WHERE user_id = ? AND position > ?'
        return self.query(sql, (diff, user_id, position), output='rowcount') > 0

    def remove_account(self, user_id: int, account_id: int) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ? AND ROWID = ?'
        return self.query(sql, (user_id, account_id), output='rowcount') == 1

    def remove_all(self, user_id: int) -> bool:
        sql = 'DELETE FROM accounts WHERE user_id = ?'
        return self.query(sql, (user_id,), output='rowcount') > 0

    def count_of_accounts(self, user_id: int) -> int:
        sql = 'SELECT COUNT(ROWID) FROM accounts WHERE user_id = ?'
        return int(self.query(sql, (user_id,), output='scalar'))


accounting: AccountingRepositoryAbstract = AccountingRepositorySQLite()
