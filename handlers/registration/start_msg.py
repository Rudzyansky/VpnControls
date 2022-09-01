from telethon.events import register, NewMessage

import domain
from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from handlers.utils import extract
from localization import translate


@register(NewMessage(access_list(Categories.REGISTERED), blacklist_chats=True, pattern=r'^/start(?: ([a-z]{2}))?$'))
@translate()
async def handler(event: NewMessage.Event, _):
    user = domain.registration.register_user(event.chat_id, extract(event.pattern_match, 1, 'en'))
    if user is None:
        await event.client.send_message(event.chat_id, _('Something went wrong. Contact with developer'))
        return

    # todo say hello
