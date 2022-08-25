from telethon import TelegramClient

from . import common


def init(client: TelegramClient):
    common._client = client


__all__ = [
    'init'
]
