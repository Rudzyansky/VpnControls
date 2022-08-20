from telethon.events import register, NewMessage

from database import tokens, users
from handlers.accesslist import users_al
from localization import translate


@register(NewMessage(users_al, blacklist_chats=True, pattern=rf'^/start$'))
@translate
async def handler(event: NewMessage.Event, _):
    if not tokens.check_user(event.chat_id):
        return
    users.add_user(event.chat_id)
    # todo say hello
