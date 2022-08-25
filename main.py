#!/usr/bin/env python3
# encoding=utf-8
import asyncio
from os import getenv

from telethon import TelegramClient

import domain
import handlers


async def main():
    client = TelegramClient('vpn', int(getenv('API_ID')), getenv('API_HASH'))
    client.parse_mode = 'markdown'
    await client.start(bot_token=getenv('TOKEN'))
    domain.init(client)
    handlers.register(client)
    print('Ready')
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
