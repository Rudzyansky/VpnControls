from telethon.events import register, NewMessage

from domain import users
from handlers.utils import extract
from localization import translate


@register(NewMessage(users.registered, blacklist_chats=True, pattern=r'^/start(?: ([a-z]{2}))?$'))
@translate(text=False)
async def handler(event: NewMessage.Event):
    if not users.is_accept_invite(event.chat_id):
        return
    users.add_user(event.chat_id, extract(event.pattern_match, 1, 'en'))
    # todo say hello
