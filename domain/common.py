from typing import Any, Coroutine

from telethon import TelegramClient

import database
from entities.user import User

_client: TelegramClient
_users = database.common.get_all_users()
_languages: dict[int, str] = {u.id: u.language for u in _users}


def client(*args, **kwargs) -> Coroutine[Any, Any, Any]:
    return _client(*args, **kwargs)


async def get_entity(user_id: int):
    return await _client.get_entity(user_id)


def language(user_id: int):
    return _languages[user_id]


def update_language(user: User):
    _languages[user.id] = user.language
