from functools import wraps
from gettext import translation, NullTranslations

from telethon.events.common import EventCommon

from domain import users

localedir = 'lang'
languages = ['en', 'ru']


def load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def translate(text=True, nums_text=False, translations=False):
    def decorator(func):
        def inject_translations(data):
            setattr(func, 'translations', data)

        setattr(func, inject_translations.__name__, inject_translations)

        @wraps(func)
        def wrapper(event: EventCommon):
            t = func.translations[users.language(event.chat_id)]
            kwargs = {}
            if text:
                kwargs['_'] = t.gettext
            if nums_text:
                kwargs['_n'] = t.ngettext
            if translations:
                kwargs['t'] = func.translations
            return func(event, **kwargs)

        return wrapper

    return decorator
