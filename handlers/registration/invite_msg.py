from telethon.events import register, NewMessage

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.registration.utils import generate_invite_text, generate_buttons
from localization import translate


def handler_filter(event: NewMessage.Event):
    return event.chat_id in access_list(Categories.HAS_ACTUAL_TOKENS)


@register(NewMessage(func=handler_filter, pattern='^/invite$'))
@translate()
async def handler(event: NewMessage.Event, _):
    offset, count, token = domain.registration.get_actual_token(event.chat_id)
    text = await generate_invite_text(event.client, token, count, _=_)
    buttons = generate_buttons(event.client, token, offset, count, _=_) if token is not None else None
    await event.client.send_message(event.chat_id, text, buttons=buttons)
