from datetime import datetime

from telethon.events import register, CallbackQuery

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from entities.token import Token
from localization import translate
from utils import contact_with_developer


@translate(False, translations=True)
async def handler_filter(event: CallbackQuery.Event, translations):
    _ = translations[event.pattern_match[2].decode()].gettext
    registered = event.sender_id in access_list(Categories.REGISTERED)
    if registered:
        await event.answer(_('Access denied'))
    return not registered


@register(CallbackQuery(func=handler_filter, pattern=rb'(?s)^accept (.{16}) ([a-z]{2})$'))
@translate(False, translations=True)
async def handler(event: CallbackQuery.Event, translations):
    lang = event.pattern_match[2].decode()
    _ = translations[lang].gettext
    token = domain.registration.get_token(event.pattern_match[1])
    if token is None or (token.used_by is not None and token.used_by != event.sender_id):
        await event.answer(_('Invitation is invalid'))
        return

    token.used_by = event.sender_id
    if domain.registration.use_token(token):
        _un = (await event.client.get_me()).username
        await event.answer(url=f'https://t.me/{_un}?start={lang}')
    else:
        await event.answer(_('An error has occurred. Please contact your administrator'))
        await event.client.send_message(event.chat_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='accept',
            sender_id=event.sender_id,
        ))
