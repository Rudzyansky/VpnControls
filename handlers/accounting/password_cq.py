from datetime import datetime

from telethon.errors import MessageNotModifiedError
from telethon.events import register, CallbackQuery

import domain.accounting
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.accounting.utils import generate_credentials_text, generate_buttons
from localization import translate
from utils import contact_with_developer


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.HAS_ACCOUNTS)


@register(CallbackQuery(func=handler_filter, pattern=rb'^password ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    result = domain.accounting.reset_password(event.sender_id, int(event.pattern_match[1]))
    if result.data is None:
        await event.client.send_message(event.sender_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='password',
            data=event.data,
            sender_id=event.sender_id,
            chat_id=event.chat_id,
        ))
        return

    if result.changed:
        text = generate_credentials_text(result.data, _)
        buttons = generate_buttons(event.client, result.data, _=_)
        try:
            await event.edit(text, buttons=buttons)
        except MessageNotModifiedError:
            pass
    else:
        await event.answer()
