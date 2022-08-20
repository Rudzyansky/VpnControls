from telethon.events import register, CallbackQuery

from database import tokens
from handlers.accesslist import admins_al
from handlers.token import Token
from . import translations


@register(CallbackQuery(pattern=rb'^revoke (.{16})$'))
async def handler(event: CallbackQuery.Event):
    # user = users[event.chat_id]
    # t = translations[user.language]
    # _ = t.gettext

    if event.sender_id not in admins_al:
        await event.answer(_('Access denied'))
        return

    start, end = event.data_match.regs[1]
    if tokens.revoke(Token(event.data[start:end], owner_id=event.chat_id)):
        await event.edit(_('Invitation turned into a pumpkin'))
    else:
        await event.edit(_('Invitation is invalid'))
