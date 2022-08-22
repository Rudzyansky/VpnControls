from telethon.events import register, NewMessage

from domain import registration, common
from handlers.utils import extract
from localization import translate


@register(NewMessage(common.registered, blacklist_chats=True, pattern=r'^/start(?: ([a-z]{2}))?$'))
@translate(text=False)
async def handler(event: NewMessage.Event):
    if not registration.is_accept_invite(event.chat_id):
        return
    registration.register_user(event.chat_id, extract(event.pattern_match, 1, 'en'))
    # todo say hello
