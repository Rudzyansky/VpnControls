import database
from bot_commands.categories import Categories
from database.abstract import Connection
from entities.token import Token
from entities.user import User
from . import common, commands


@database.connection()
def register_user(user_id: int, language: str, c: Connection):
    success = database.registration.add_user(User(id=user_id, language=language), c)
    if success:
        database.registration.revoke_token_by_user_id(user_id, c)
        user = database.common.get_user(user_id, c)
        common.update_language(user)
        commands.set_categories(user, Categories.COMMON, Categories.NO_ACCOUNTS)
        return user
    return None


def is_accept_invite(user_id: int):
    return database.registration.is_accept_invite(user_id)


def revoke_token(token: Token):
    return database.registration.revoke_token(token.bytes, token.owner_id)


@database.connection()
def create_token(user_id: int, c: Connection):
    token = Token(owner_id=user_id)
    success = database.registration.add_token(token.bytes, token.owner_id, c)
    if success:
        return database.registration.get_token(token.bytes, token.owner_id, c)
    return None


def get_tokens_limit(user_id: int):
    """
    Get all tokens owned by user_id
    """
    return database.registration.get_tokens_limit(user_id)


def get_tokens(user_id: int):
    """
    Get all tokens owned by user_id
    """
    return database.registration.get_all_tokens(user_id)


def get_current_tokens(user_id: int) -> list[Token]:
    """
    Get non-revoked tokens owned by user_id
    """
    return database.registration.get_actual_tokens(user_id)


def fetch_token(token: Token):
    """
    Fetch all token's data by token + owner_id
    """
    return database.registration.get_token(token.bytes, token.owner_id)


@database.connection()
def use_token(token: Token):
    database.registration.free_token_by_user_id(token.used_by)
    return database.registration.use_token(token.bytes, token.owner_id, token.used_by)
