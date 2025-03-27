import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler

import domain
from handlers.filters import has_actual_tokens
from handlers.registration.utils import generate_invite_text, generate_buttons
from localization import LocalizedContext

pattern = re.compile(r'^invite ([0-9]+)$')


async def handler(update: Update, context: LocalizedContext):
    if not has_actual_tokens.filter(update):
        return

    position = int(context.match.group(1))

    offset, count, token = domain.registration.get_actual_token(context.chat_id, position)
    text = generate_invite_text(context, token, count)
    buttons = generate_buttons(context, token, offset, count) if token is not None else None
    await update.effective_message.edit_text(text, reply_markup=buttons, parse_mode=ParseMode.HTML)


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
