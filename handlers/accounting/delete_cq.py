from telethon.events import register, CallbackQuery

import domain.accounting
from localization import translate


@register(CallbackQuery(pattern=rb'^delete ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    domain.accounting.delete_account(event.sender_id, int(event.pattern_match[1]))
    await event.edit(_('Account removed'))
