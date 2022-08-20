import os
from functools import wraps
from gettext import translation, NullTranslations
from pathlib import Path

from telethon.events.common import EventCommon

from domain import users

localedir = 'lang'
languages = ['en', 'ru']


def load_translations(domain: str) -> dict[str:NullTranslations]:
    domain = domain.split('.')[-1]
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def translate(text=True, current=False, translations=False):
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
            if current:
                kwargs['t'] = t
            if translations:
                kwargs['translations'] = func.translations
            return func(event, **kwargs)

        return wrapper

    return decorator
