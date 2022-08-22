from importlib import import_module
from types import FunctionType

from telethon import TelegramClient

from . import registration, privileges, accounting, settings

flows = [registration, privileges, accounting, settings]

_HANDLERS_ATTRIBUTE = '__tl.handlers'  # telethon/events/__init__.py


def handlers(module):
    for item in dir(module):
        a = getattr(module, item)
        if isinstance(a, FunctionType) and hasattr(a, _HANDLERS_ATTRIBUTE):
            yield a


def register(client: TelegramClient):
    for flow in flows:
        for module_name in flow.modules:
            module = import_module('.' + module_name, flow.__name__)
            for func in handlers(module):
                client.add_event_handler(func)


__all__ = [
    'register'
]
