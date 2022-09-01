from telethon.events import register, NewMessage

import domain.commands
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate


def handler_filter(event: NewMessage.Event):
    return event.chat_id in access_list(Categories.REGISTERED)


@register(NewMessage(func=handler_filter, pattern=r'^/refresh$'))
@translate()
async def handler(event: NewMessage.Event, _):
    await domain.commands.telegram_set_commands(event.chat_id)
    await event.client.delete_messages(event.chat_id, event.message.id)
