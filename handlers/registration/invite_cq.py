from telethon.events import register, CallbackQuery

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.registration.utils import generate_invite_text, generate_buttons
from localization import translate


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.HAS_ACTUAL_TOKENS)


@register(CallbackQuery(func=handler_filter, pattern=rb'^invite ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    offset, count, token = domain.registration.get_actual_token(event.chat_id, int(event.pattern_match[1]))
    text = await generate_invite_text(event.client, token, count, _=_)
    buttons = generate_buttons(event.client, token, offset, count, _=_) if token is not None else None
    await event.edit(text, buttons=buttons)
