from telethon.events import register, NewMessage

from domain import users
from localization import translate


@register(NewMessage(users.registered, blacklist_chats=True, pattern=rf'^/start$'))
@translate
async def handler(event: NewMessage.Event, _):
    if not users.is_accept_invite(event.chat_id):
        return
    users.add_user(event.chat_id)
    # todo say hello
