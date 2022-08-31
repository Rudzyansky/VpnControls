from telethon import TelegramClient

from . import common, commands


async def init(client: TelegramClient):
    common.client = client
    await commands.init()


__all__ = [
    'init'
]
