#!/usr/bin/env python3
# encoding=utf-8
import asyncio

from telethon import TelegramClient

import domain
import env
import handlers


async def main():
    client = TelegramClient(env.TOKEN.split(':')[0], env.API_ID, env.API_HASH)
    client.parse_mode = 'markdown'
    await client.start(bot_token=env.TOKEN)
    await domain.init(client)
    handlers.register(client)
    print('Ready')
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
