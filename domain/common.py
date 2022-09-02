from telethon import TelegramClient

import database

client: TelegramClient
_languages: dict[int, str]


@database.connection()
def _init(c):
    global _languages
    _languages = {u.id: u.language for u in database.common.get_all_users(c)}


_init()


def language(user_id: int):
    global _languages
    return _languages[user_id]


@database.connection()
def update_language(user_id: int, lang_code: str, c):
    global _languages
    database.common.set_language(user_id, lang_code, c)
    _languages[user_id] = lang_code


def update_language_cache(user_id: int, lang_code: str):
    global _languages
    _languages[user_id] = lang_code
