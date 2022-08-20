import database
from .users import Users

users: Users = Users(
    database.users,
    database.tokens
)

__all__ = [
    'users'
]
