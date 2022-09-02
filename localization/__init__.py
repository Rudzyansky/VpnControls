import os.path
from functools import wraps
from gettext import translation, NullTranslations

from telethon.events.common import EventCommon

from env import ROOT
from localization.languages import _langs

localedir = 'lang'

if localedir[0] != '/':
    localedir = os.path.join(ROOT, localedir)

# languages = [k for k, v in _langs.items()]
languages = _langs

_cache: dict[str:dict[str:NullTranslations]] = {}


def _load_translations(domain: str) -> dict[str:NullTranslations]:
    return {i: translation(domain, localedir, [i], fallback=True) for i in languages}


def _get_translations(domain: str) -> dict[str:NullTranslations]:
    if _cache.get(domain) is None:
        _cache[domain] = _load_translations(domain)
    return _cache[domain]


def get_translations(package_name: str = None,
                     module_name: str = None,
                     domain: str = None) -> dict[str:NullTranslations]:
    if package_name is not None and module_name is None and domain is None:
        return _get_translations(package_name.split('.')[-1])
    elif package_name is None and module_name is not None and domain is None:
        return _get_translations(module_name.split('.')[-2])
    elif package_name is None and module_name is None and domain is not None:
        return _get_translations(domain)
    else:
        raise RuntimeError('get_translations: wrong input: ' +
                           str({'package_name': package_name, 'module_name': module_name, 'domain': domain}))


def translate(text=True, current=False, translations=False):
    def decorator(func):
        setattr(func, 'translations', get_translations(module_name=func.__module__))
        from domain import common

        @wraps(func)
        def wrapper(event: EventCommon):
            kwargs = {}
            if text:
                kwargs['_'] = func.translations[common.language(event.chat_id)].gettext
            if current:
                kwargs['t'] = func.translations[common.language(event.chat_id)]
            if translations:
                kwargs['translations'] = func.translations
            return func(event, **kwargs)

        return wrapper

    return decorator
