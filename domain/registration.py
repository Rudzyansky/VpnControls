from typing import Optional

import database
import domain
from database.abstract import Connection
from domain.types import CategoriesUpdater
from entities.token import Token
from entities.user import User


@database.connection(manual=True)
async def register_user(user_id: int, language: str, c: Connection):
    c.open()
    c.begin_transaction()
    success = database.registration.add_user(User(id=user_id, language=language), c=c)
    if not success:
        return None

    database.registration.revoke_token_by_user_id(user_id, c=c)
    user = database.common.get_user(user_id, c)
    domain.common.update_language_cache(user.id, user.language)

    count_of_accounts = database.accounting.count_of_accounts(user_id, c=c)
    count_of_tokens = database.registration.count_of_tokens(user_id, c=c)
    count_of_actual_tokens = database.registration.count_of_actual_tokens(user_id, c=c)

    await CategoriesUpdater(user.id) \
        .registered() \
        .can_create_account(count_of_accounts, user.accounts_limit) \
        .has_accounts(count_of_accounts) \
        .can_issue_token(count_of_tokens, user.tokens_limit) \
        .has_tokens(count_of_tokens) \
        .has_actual_tokens(count_of_actual_tokens) \
        .finish(c)

    c.end_transaction()
    c.close()

    return user


@database.connection(False)
def is_accept_invite(user_id: int, c: Connection):
    return database.registration.is_accept_invite(user_id, c=c)


@database.connection(manual=True)
async def revoke_token(token: Token, c: Connection):
    c.open()
    c.begin_transaction()
    revoked = database.registration.revoke_token(token.bytes, token.owner_id, c=c)
    actual_tokens = database.registration.count_of_actual_tokens(token.owner_id, c=c)

    await CategoriesUpdater(token.owner_id) \
        .has_actual_tokens(actual_tokens) \
        .finish(c)

    c.end_transaction()
    c.close()
    return revoked


@database.connection(manual=True)
async def create_token(user_id: int, c: Connection):
    c.open()
    tokens = database.registration.count_of_tokens(user_id, c=c)
    limit = database.registration.get_tokens_limit(user_id, c=c)

    if tokens >= limit:
        c.close()
        return None

    token = Token(owner_id=user_id)

    c.begin_transaction()
    success = database.registration.add_token(token.bytes, user_id, c=c)
    if not success:
        c.close()
        return None

    actual_tokens = database.registration.count_of_actual_tokens(user_id, c=c)

    await CategoriesUpdater(user_id) \
        .can_issue_token(tokens + 1, limit) \
        .has_tokens(tokens) \
        .has_actual_tokens(actual_tokens) \
        .finish(c)

    c.end_transaction()

    token_result = database.registration.get_token(token.bytes, user_id, c=c)
    c.close()
    return token_result


@database.connection(False)
def get_tokens_limit(user_id: int, c: Connection):
    """
    Get all tokens owned by user_id
    """
    return database.registration.get_tokens_limit(user_id, c=c)


@database.connection(False)
def get_tokens(user_id: int, c: Connection):
    """
    Get all tokens owned by user_id
    """
    return database.registration.get_all_tokens(user_id, c=c)


@database.connection(False)
def get_current_tokens(user_id: int, c: Connection) -> list[Token]:
    """
    Get non-revoked tokens owned by user_id
    """
    return database.registration.get_actual_tokens(user_id, c=c)


@database.connection(False)
def get_actual_token(user_id: int, offset: int = 0, c: Connection = None) -> tuple[int, int, Optional[Token]]:
    """
    Get non-revoked token owned by user_id
    """
    count = database.registration.count_of_actual_tokens(user_id, c=c)
    if 0 <= offset < count:
        token = database.registration.get_next_actual_token(user_id, offset, c=c)
    else:
        token = None
    return offset, count, token


@database.connection(False)
def fetch_token(token: Token, c: Connection):
    """
    Fetch all token's data by token + owner_id
    """
    return database.registration.get_token(token.bytes, token.owner_id, c=c)


@database.connection()
def use_token(token: Token, c: Connection):
    database.registration.free_token_by_user_id(token.used_by, c=c)
    return database.registration.use_token(token.bytes, token.owner_id, token.used_by, c=c)
