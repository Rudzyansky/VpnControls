from datetime import datetime

from telethon.events import register, CallbackQuery

import utils
from domain import users
from entities.token import Token
from localization import translate


@register(CallbackQuery(pattern=rb'^accept (.{16}) ([a-z]{2})$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    if event.sender_id in users.registered:
        await event.answer(_('Access denied'))
        return

    token = users.fetch_token(Token(event.pattern_match[1], owner_id=event.chat_id))
    if token is None or (token.used_by is not None and token.used_by != event.sender_id):
        await event.edit(_('Invitation is invalid'))
        return

    token.used_by = event.sender_id
    if users.use_token(token):
        _un = (await event.client.get_me()).username
        await event.answer(url=f'https://t.me/{_un}?start={event.pattern_match[2]}')
    else:
        await event.answer(_('An error has occurred. Please contact your administrator'))
        payload = utils.debug_payload(chat_id=event.chat_id, sender_id=event.sender_id,
                                      timestamp=datetime.utcnow())
        text = _('Something went wrong. Contact the developer') + '\n\n' + payload
        await event.client.send_message(event.chat_id, text)
