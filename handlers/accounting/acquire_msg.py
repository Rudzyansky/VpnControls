from telethon.events import register, NewMessage
from telethon.utils import get_display_name

import domain.common
from bot_commands.categories import Categories
from domain import accounting
from domain.commands import access_list
from handlers.accounting.utils import generate_buttons, generate_credentials_text
from localization import translate


@register(NewMessage(access_list(Categories.CAN_CREATE_ACCOUNT), pattern=r'^/acquire$'))
@translate()
async def handler(event: NewMessage.Event, _):
    if event.sender.username:
        username = event.sender.username
    else:
        username = get_display_name(event.sender)

    account = domain.accounting.create_account(event.chat_id, username)
    text = generate_credentials_text(account, _)
    buttons = generate_buttons(event.client, account, _=_)
    await event.client.send_message(event.chat_id, text, buttons=buttons)
