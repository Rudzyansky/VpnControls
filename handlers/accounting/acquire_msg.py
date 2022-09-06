from datetime import datetime

from telethon.events import register, NewMessage
from telethon.utils import get_display_name

import domain.common
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.accounting.utils import generate_buttons, generate_credentials_text
from localization import translate
from utils import contact_with_developer


def handler_filter(event: NewMessage.Event):
    return event.chat_id in access_list(Categories.CAN_CREATE_ACCOUNT)


@register(NewMessage(func=handler_filter, pattern=r'^/acquire$'))
@translate()
async def handler(event: NewMessage.Event, _):
    if event.sender.username:
        username = event.sender.username
    else:
        username = get_display_name(event.sender)

    account = await domain.accounting.create_account(event.chat_id, username)
    if account is not None:
        text = generate_credentials_text(account, _)
        buttons = generate_buttons(event.client, account, _=_)
        await event.client.send_message(event.chat_id, text, buttons=buttons)
    else:
        await event.client.send_message(event.chat_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='acquire',
            chat_id=event.chat_id,
            username=username,
        ))
