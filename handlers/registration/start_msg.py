from telethon.events import register, NewMessage

import domain
from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from handlers.utils import extract
from localization import translate


def handler_filter(event: NewMessage.Event):
    registered = event.chat_id in access_list(Categories.REGISTERED)
    accepted_invite = domain.registration.is_accept_invite(event.chat_id)
    return not registered and accepted_invite


@register(NewMessage(func=handler_filter, pattern=r'^/start(?: ([a-z]{2}))?$'))
@translate()
async def handler(event: NewMessage.Event, _):
    user = domain.registration.register_user(event.chat_id, extract(event.pattern_match, 1, 'en'))
    if user is None:
        await event.client.send_message(event.chat_id, _('Something went wrong. Contact with developer'))
        return

    # todo say hello
