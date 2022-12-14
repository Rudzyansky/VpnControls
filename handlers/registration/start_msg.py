from telethon.events import register, NewMessage

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.utils import extract
from localization import translate


def handler_filter(event: NewMessage.Event):
    registered = event.chat_id in access_list(Categories.REGISTERED)
    accepted_invite = domain.registration.is_accept_invite(event.chat_id)
    return not registered and accepted_invite


@register(NewMessage(func=handler_filter, pattern=r'^/start(?: ([a-z]{2}))?$'))
@translate(text=False, translations=True)
async def handler(event: NewMessage.Event, translations):
    lang = extract(event.pattern_match, 1, 'en')
    user = await domain.registration.register_user(event.chat_id, lang)
    if user is None:
        _ = translations['en'].gettext
        await event.client.send_message(event.chat_id, _('Something went wrong. Contact with developer'))
        return

    _ = translations[user.language].gettext

    # todo say hello
