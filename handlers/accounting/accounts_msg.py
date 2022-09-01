from datetime import datetime

from telethon.events import register, NewMessage

import domain.common
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.accounting.utils import generate_buttons, generate_credentials_text
from localization import translate
from utils import contact_with_developer


def handler_filter(event: NewMessage.Event):
    return event.chat_id in access_list(Categories.HAS_ACCOUNTS)


@register(NewMessage(func=handler_filter, pattern=r'^/accounts$'))
@translate()
async def handler(event: NewMessage.Event, _):
    account_data = domain.accounting.get_account(event.chat_id, 0)
    if account_data:
        offset, count, account = account_data
        text = generate_credentials_text(account, _)
        buttons = generate_buttons(event.client, account, offset, count, _)
        await event.client.send_message(event.chat_id, text, buttons=buttons)
    else:
        await event.client.send_message(event.chat_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='accounts',
            chat_id=event.chat_id,
        ))
