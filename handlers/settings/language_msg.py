from telethon import Button
from telethon.events import register, NewMessage

import domain.common
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate, languages, get_translations


@register(NewMessage(access_list(Categories.REGISTERED), pattern=r'^/language$'))
@translate()
async def handler(event: NewMessage.Event, _):
    text = _('Choose language')
    t = get_translations(domain='languages')[domain.common.language(event.chat_id)]
    full = [Button.inline(t.gettext(_lang_code), f'language {_lang_code}') for _lang_code in languages]
    buttons_matrix = [full[i:i + 2] for i in range(0, len(full), 2)]  # split by 2
    buttons = event.client.build_reply_markup(buttons_matrix, inline_only=True)
    await event.client.send_message(event.chat_id, text, buttons=buttons)
