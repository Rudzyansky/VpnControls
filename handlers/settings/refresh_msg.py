from telethon.events import register, NewMessage

import domain.commands
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate


@register(NewMessage(access_list(Categories.REGISTERED), pattern=r'^/refresh$'))
@translate()
async def handler(event: NewMessage.Event, _):
    await domain.commands.refresh_commands(event.chat_id)
    await event.client.delete_messages(event.chat_id, event.message.id)
