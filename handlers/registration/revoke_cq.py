from telethon.events import register, CallbackQuery

from domain import users
from entities.token import Token
from localization import translate


@register(CallbackQuery(pattern=rb'^revoke (.{16})$'))
@translate
async def handler(event: CallbackQuery.Event, _):
    if event.sender_id not in users.admins:
        await event.answer(_('Access denied'))
        return

    start, end = event.data_match.regs[1]
    if tokens.revoke(Token(event.data[start:end], owner_id=event.chat_id)):
        await event.edit(_('Invitation turned into a pumpkin'))
    else:
        await event.edit(_('Invitation is invalid'))
