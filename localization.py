from functools import wraps
from gettext import translation, NullTranslations

from telethon.events.common import EventCommon

from domain import users

localedir = 'lang'
languages = ['en', 'ru']


def load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def translate(func):
    setattr(func, 'inject_translations', lambda data: setattr(func, 'translations', data))

    @wraps(func)
    def wrapper(event: EventCommon):
        t = func.translations[users.language(event.chat_id)]
        return func(event, _=t.gettext, _n=t.ngettext)

    return wrapper
