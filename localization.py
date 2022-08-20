from functools import wraps
from gettext import translation, NullTranslations

from telethon.events.common import EventCommon

localedir = 'lang'
languages = ['en', 'ru']

_TRANSLATIONS_ATTRIBUTE = '__translations'


def load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def translate(func):
    translations = getattr(func, _TRANSLATIONS_ATTRIBUTE)

    @wraps(func)
    def wrapper(event: EventCommon):
        t = translations[users.language(event.chat_id)]
        return func(event, _=t.gettext, _n=t.ngettext)

    return wrapper
