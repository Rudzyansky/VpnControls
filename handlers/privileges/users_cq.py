from telethon.events import register, NewMessage, CallbackQuery

from domain import privileges
from domain.entities.users_meta import UsersMeta
from handlers.privileges.utils import generate_users_message
from localization import translate


@register(CallbackQuery(pattern=rb'^users ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    page = int(event.pattern_match[1])
    data: UsersMeta = await privileges.get_users(event.sender_id, page)
    text, buttons = generate_users_message(event.client, data, _)
    await event.edit(text, buttons=buttons)
