from datetime import datetime

from telethon.errors import MessageNotModifiedError
from telethon.events import register, CallbackQuery

import domain.accounting
from handlers.accounting.utils import generate_credentials_text, generate_buttons
from localization import translate
from utils import contact_with_developer


@register(CallbackQuery(pattern=rb'^password ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    account = domain.accounting.reset_password(event.sender_id, int(event.pattern_match[1]))
    if account is not None:
        try:
            await event.edit(generate_credentials_text(account, _),
                             buttons=generate_buttons(event.client, account, _=_))
        except MessageNotModifiedError:
            pass
    else:
        await event.client.send_message(event.sender_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='password',
            data=event.data,
            sender_id=event.sender_id,
            chat_id=event.chat_id,
        ))
