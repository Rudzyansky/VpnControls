from typing import Optional

import domain
from db import Repository
from domain.types import CategoriesUpdater
from entities.token import Token
from entities.user import User


async def register_user(user_id: int, language: str):
    success = Repository.Registration.add_user(User(id=user_id, language=language))
    if not success:
        return None

    Repository.Registration.revoke_token_by_user_id(user_id)
    user = Repository.Common.get_user(user_id)
    domain.common.update_language_cache(user.id, user.language)

    count_of_accounts = Repository.Accounting.count_of_accounts(user_id)
    count_of_tokens = Repository.Registration.count_of_tokens(user_id)
    count_of_actual_tokens = Repository.Registration.count_of_actual_tokens(user_id)

    await CategoriesUpdater(user.id) \
        .registered() \
        .can_create_account(count_of_accounts, user.accounts_limit) \
        .has_accounts(count_of_accounts) \
        .can_issue_token(count_of_tokens, user.tokens_limit) \
        .has_tokens(count_of_tokens) \
        .has_actual_tokens(count_of_actual_tokens) \
        .finish()

    return user


def is_accept_invite(user_id: int):
    return Repository.Registration.is_accept_invite(user_id)


async def revoke_token(token: bytes, owner_id: int):
    success = Repository.Registration.revoke_token(token, owner_id)
    if not success:
        return None

    user = Repository.Common.get_user(owner_id)
    count_of_accounts = Repository.Accounting.count_of_accounts(owner_id)
    count_of_tokens = Repository.Registration.count_of_tokens(owner_id)
    count_of_actual_tokens = Repository.Registration.count_of_actual_tokens(owner_id)

    await CategoriesUpdater(owner_id) \
        .can_create_account(count_of_accounts, user.accounts_limit) \
        .has_accounts(count_of_accounts) \
        .can_issue_token(count_of_tokens, user.tokens_limit) \
        .has_tokens(count_of_tokens) \
        .has_actual_tokens(count_of_actual_tokens) \
        .finish()

    return user


async def revoke_token_force(token: bytes):
    t = Repository.Registration.get_token(token)
    if t is None:
        return False
    revoked = Repository.Registration.revoke_token(token, t.owner_id)
    actual_tokens = Repository.Registration.count_of_actual_tokens(t.owner_id)

    await CategoriesUpdater(t.owner_id) \
        .has_actual_tokens(actual_tokens) \
        .finish()

    return revoked


async def create_token(user_id: int):
    tokens = Repository.Registration.count_of_tokens(user_id)
    limit = Repository.Registration.get_tokens_limit(user_id)

    if tokens >= limit:
        return None

    token = Token(owner_id=user_id)

    success = Repository.Registration.add_token(token.bytes, user_id)
    if not success:
        return None

    actual_tokens = Repository.Registration.count_of_actual_tokens(user_id)

    await CategoriesUpdater(user_id) \
        .can_issue_token(tokens + 1, limit) \
        .has_tokens(tokens) \
        .has_actual_tokens(actual_tokens) \
        .finish()

    return Repository.Registration.fetch_token(token.bytes, user_id)


def get_tokens_limit(user_id: int):
    """
    Get all tokens owned by user_id
    """
    return Repository.Registration.get_tokens_limit(user_id)


def get_tokens(user_id: int):
    """
    Get all tokens owned by user_id
    """
    return Repository.Registration.get_all_tokens(user_id)


def get_current_tokens(user_id: int) -> list[Token]:
    """
    Get non-revoked tokens owned by user_id
    """
    return Repository.Registration.get_actual_tokens(user_id)


def get_actual_token(user_id: int, offset: int = 0) -> tuple[int, int, Optional[Token]]:
    """
    Get non-revoked token owned by user_id
    """
    count = Repository.Registration.count_of_actual_tokens(user_id)
    if 0 <= offset < count:
        token = Repository.Registration.get_next_actual_token(user_id, offset)
    else:
        token = None
    return offset, count, token


def get_token(token: bytes):
    """
    Fetch all token's data by token + owner_id
    """
    return Repository.Registration.get_token(token)


def fetch_token(token: Token):
    """
    Fetch all token's data by token + owner_id
    """
    return Repository.Registration.fetch_token(token.bytes, token.owner_id)


def use_token(token: Token):
    Repository.Registration.free_token_by_user_id(token.used_by)
    return Repository.Registration.use_token(token.bytes, token.owner_id, token.used_by)
