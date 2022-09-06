from telethon.events import register, CallbackQuery

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.HAS_ACTUAL_TOKENS)


@register(CallbackQuery(func=handler_filter, pattern=rb'(?s)^revoke (.{16})$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    if await domain.registration.revoke_token(event.pattern_match[1], event.chat_id):
        await event.edit(_('Invitation turned into a pumpkin'))
    else:
        await event.edit(_('Invitation is invalid'))
