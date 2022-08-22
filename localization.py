from functools import wraps
from gettext import translation, NullTranslations

from telethon.events.common import EventCommon

localedir = 'lang'
languages = ['en', 'ru']

_cache: dict[str:dict[str:NullTranslations]] = {}


def _load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def _get_translations(domain: str) -> dict[str:NullTranslations]:
    if _cache.get(domain) is None:
        _cache[domain] = _load_translations(domain)
    return _cache[domain]


def get_translations(package_name: str = None, module_name: str = None) -> dict[str:NullTranslations]:
    if package_name is not None and module_name is None:
        return _get_translations(package_name.split('.')[-1])
    elif package_name is None and module_name is not None:
        return _get_translations(module_name.split('.')[-2])
    else:
        raise RuntimeError('get_translations: wrong input: ' +
                           str({'package_name': package_name, 'module_name': module_name}))


def translate(text=True, current=False, translations=False):
    def decorator(func):
        setattr(func, 'translations', get_translations(module_name=func.__module__))
        from domain import common

        @wraps(func)
        def wrapper(event: EventCommon):
            t = func.translations[common.language(event.chat_id)]
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
