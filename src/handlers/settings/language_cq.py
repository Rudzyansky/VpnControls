import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.settings.utils import generate_text, generate_buttons
from localization import LocalizedContext

pattern = re.compile('^language ([a-z]{2})$')


async def handler(update: Update, context: LocalizedContext):
    input_lang_code = context.match.group(1)
    languages = context.localize('settings.language')
    if input_lang_code not in languages.keys():
        await update.callback_query.answer(context.localize('settings.unknown_language') % input_lang_code)
    domain.common.update_language(context.chat_id, input_lang_code)
    domain.commands.recalculate_commands(context.chat_id)
    await domain.commands.telegram_set_commands(context.chat_id)
    await update.callback_query.answer(context.localize('settings.language_changed', input_lang_code))

    text = generate_text(context)
    buttons = generate_buttons(context)
    try:
        await update.effective_message.edit_text(text, reply_markup=buttons)
    except Exception:
        pass


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
