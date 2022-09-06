from telethon import TelegramClient

from domain import common, commands, registration, accounting


async def init(client: TelegramClient):
    common.client = client
    await commands.init()


__all__ = [
    'init',
    'common',
    'commands',
    'registration',
    'accounting',
]
