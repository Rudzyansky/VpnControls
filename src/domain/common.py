from typing import Optional, List

from telegram import LinkPreviewOptions
from telegram.constants import ParseMode
from telegram.ext import Application, Defaults, AIORateLimiter, ContextTypes

import config
from db import Repository
from entities.user import User
from localization import LocalizedContext


def application_factory():
    builder = Application.builder()
    builder.token(config.TELEGRAM_BOT_TOKEN)
    builder.defaults(Defaults(parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True)))
    builder.rate_limiter(AIORateLimiter(max_retries=10))
    builder.context_types(ContextTypes(context=LocalizedContext))
    return builder.build()


application: Application = application_factory()
_languages: dict[int, str]


def load_languages_cache():
    global _languages
    _languages = {u.id: u.language for u in Repository.Common.get_all_users()}


def language(user_id: int):
    global _languages
    return _languages.get(user_id, 'en')


def update_language(user_id: int, lang_code: str):
    global _languages
    Repository.Common.set_language(user_id, lang_code)
    _languages[user_id] = lang_code


def update_language_cache(user_id: int, lang_code: str):
    global _languages
    _languages[user_id] = lang_code


def get_all_users() -> List[User]:
    return Repository.Common.get_all_users()


def get_user(user_id: int) -> Optional[User]:
    return Repository.Common.get_user(user_id)
