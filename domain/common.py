from telethon import TelegramClient

import database

client: TelegramClient
_languages: dict[int, str] = {u.id: u.language for u in database.common.get_all_users()}


def language(user_id: int):
    return _languages[user_id]


def update_language(user_id: int, lang_code: str):
    database.common.set_language(user_id, lang_code)
    _languages[user_id] = lang_code
