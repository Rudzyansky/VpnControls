from telethon.events import register, CallbackQuery

import domain.accounting
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.HAS_ACCOUNTS)


@register(CallbackQuery(func=handler_filter, pattern=rb'^delete ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    if await domain.accounting.delete_account(event.sender_id, int(event.pattern_match[1])):
        await event.edit(_('Account removed'))
    else:
        await event.edit(_('Account NOT removed'))
