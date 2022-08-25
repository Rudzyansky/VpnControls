from telethon import TelegramClient

import database
from entities.user import User

_client: TelegramClient
_users = database.common.get_all_users()
_languages: dict[int, str] = {u.id: u.language for u in _users}


@property
def client() -> TelegramClient:
    return _client


def language(user_id: int):
    return _languages[user_id]


def update_language(user: User):
    _languages[user.id] = user.language
