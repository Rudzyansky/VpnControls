from .abstract import Accounts, Users, Tokens
from .sqlite import UsersSqlite, TokensSqlite, AccountsSqlite

users: Users = UsersSqlite()
tokens: Tokens = TokensSqlite()
accounts: Accounts = AccountsSqlite()

__all__ = [
    'users', 'tokens', 'accounts'
]
