from telethon import TelegramClient

import database
from entities.user import User

client: TelegramClient
_languages: dict[int, str] = {u.id: u.language for u in database.common.get_all_users()}


def language(user_id: int):
    return _languages[user_id]


def update_language(user: User):
    _languages[user.id] = user.language
