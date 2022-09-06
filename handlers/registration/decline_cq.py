from telethon.events import register, CallbackQuery

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from entities.token import Token
from localization import translate


@translate(False, translations=True)
async def handler_filter(event: CallbackQuery.Event, translations):
    _ = translations[event.pattern_match[2].decode()].gettext
    registered = event.sender_id in access_list(Categories.REGISTERED)
    if registered:
        await event.answer(_('Access denied'))
    return not registered


@register(CallbackQuery(func=handler_filter, pattern=rb'(?s)^decline (.{16}) ([a-z]{2})$'))
@translate(False, translations=True)
async def handler(event: CallbackQuery.Event, translations):
    _ = translations[event.pattern_match[2].decode()].gettext
    if await domain.registration.revoke_token(event.pattern_match[1]):
        await event.edit(_('Invitation turned into a pumpkin'))
    else:
        await event.answer(_('Invitation is invalid'))
