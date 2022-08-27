from telethon.events import register, CallbackQuery

import domain.accounting
from handlers.accounting.utils import generate_credentials_text, generate_buttons
from localization import translate


@register(CallbackQuery(pattern=rb'^password ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    account = domain.accounting.reset_password(event.sender_id, int(event.pattern_match[1]))
    await event.edit(generate_credentials_text(account, _), buttons=generate_buttons(event.client, account, _))
