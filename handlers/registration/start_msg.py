from telethon.events import register, NewMessage

from database import tokens, users
from handlers.accesslist import users_al
from . import translations


@register(NewMessage(users_al, blacklist_chats=True, pattern=rf'^/start$'))
async def handler(event: NewMessage.Event):
    # user = users[event.chat_id]
    # t = translations[user.language]
    # _ = t.gettext

    if not tokens.check_user(event.chat_id):
        return
    users.add_user(event.chat_id)
    # todo say hello
