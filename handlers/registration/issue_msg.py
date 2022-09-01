from datetime import datetime

from telethon.events import register, NewMessage

import domain
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.registration.utils import generate_buttons
from localization import translate
from utils import contact_with_developer


def handler_filter(event: NewMessage.Event):
    return event.chat_id in access_list(Categories.CAN_ISSUE_TOKEN)


@register(NewMessage(func=handler_filter, pattern='^/issue$'))
@translate()
async def handler(event: NewMessage.Event, _):
    token = await domain.registration.create_token(event.chat_id)
    if token is not None:
        text = _('Token `%s` issued\n__Expires in__ **%s**') % (token, token.expire)
        buttons = generate_buttons(event.client, token, _=_)
        await event.client.send_message(event.chat_id, text, buttons=buttons)
    else:
        await event.reply(contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='issue token',
            user_id=event.chat_id,
        ))
