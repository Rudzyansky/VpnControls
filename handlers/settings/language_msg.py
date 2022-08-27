from telethon import Button
from telethon.events import register, NewMessage

from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate


@register(NewMessage(access_list(Categories.REGISTERED), pattern=r'^/language$'))
@translate()
async def handler(event: NewMessage.Event, _):
    text = _('Choose language')
    buttons_matrix = [
        [
            # Button.inline(lang_name, f'lang {lang_code}'),
            # Button.inline(lang_name, f'lang {lang_code}')
        ],
    ]
    buttons = event.client.build_reply_markup(buttons_matrix, inline_only=True)
    await event.client.send_message(event.chat_id, text, reply_markup=buttons)
