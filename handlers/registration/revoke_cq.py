from telethon.events import register, CallbackQuery

from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from entities.token import Token
from localization import translate


@register(CallbackQuery(access_list(Categories.HAS_ACTUAL_TOKENS), pattern=rb'^revoke (.{16})$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    if registration.revoke_token(Token(event.pattern_match[1], owner_id=event.chat_id)):
        await event.edit(_('Invitation turned into a pumpkin'))
    else:
        await event.edit(_('Invitation is invalid'))
