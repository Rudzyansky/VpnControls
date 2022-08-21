import database
from .users import Users

users: Users = Users(
    database.common,
    database.registration
)

__all__ = [
    'users'
]
