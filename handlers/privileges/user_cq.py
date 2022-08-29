from telethon.events import register, CallbackQuery

from domain import privileges
from domain.entities.users_meta import UsersMeta
from handlers.privileges.utils import generate_users_message
from localization import translate


@register(CallbackQuery(pattern=rb'^user ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    id = int(event.pattern_match[1])
    data = await privileges.get_user_data(event.sender_id, id)
    text, buttons = generate_users_message(event.client, data, _)
    await event.edit(text, buttons=buttons)
