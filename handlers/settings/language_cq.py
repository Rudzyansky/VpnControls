from telethon.events import register, CallbackQuery

import domain.common
from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate, languages


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.REGISTERED)


@register(CallbackQuery(func=handler_filter, pattern=rb'^language ([a-z]{2})$'))
@translate(translations=True)
async def handler(event: CallbackQuery.Event, _, translations):
    input_lang_code = event.pattern_match[1].decode()
    if input_lang_code not in languages:
        await event.answer(_('Unknown language with code `%s`') % input_lang_code)
        return

    domain.common.update_language(event.chat_id, input_lang_code)
    domain.commands.recalculate_commands(event.chat_id)
    await domain.commands.telegram_set_commands(event.chat_id)
    await event.answer(translations[input_lang_code].gettext('Language changed'))
