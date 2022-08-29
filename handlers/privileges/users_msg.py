from telethon.events import register, NewMessage

from bot_commands.categories import Categories
from domain import privileges
from domain.commands import access_list
from domain.entities.users_meta import UsersMeta
from handlers.privileges.utils import generate_users_message
from localization import translate


@register(NewMessage(access_list(Categories.HAS_USERS), pattern=r'^/users$'))
@translate()
async def handler(event: NewMessage.Event, _):
    data: UsersMeta = await privileges.get_users(event.chat_id)
    text, buttons = generate_users_message(event.client, data, _)
    await event.client.send_message(event.chat_id, text, buttons=buttons)
