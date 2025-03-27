import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.accounting.utils import generate_credentials_buttons, generate_credentials_text
from handlers.filters import has_accounts
from localization import LocalizedContext
from utils import contact_with_developer

pattern = re.compile(r'^accounts ([0-9]+)$')


async def handler(update: Update, context: LocalizedContext):
    if not has_accounts.filter(update):
        return

    position = int(context.match.group(1))

    result = domain.accounting.get_account(update.effective_chat.id, position)
    if result.data is None:
        await update.effective_chat.send_message(
            text=contact_with_developer(context, action='accounts'),
        )
        return

    text = generate_credentials_text(context, result.data)
    keyboard = generate_credentials_buttons(context, result.data, result.offset, result.count)
    await update.effective_message.edit_text(text, reply_markup=keyboard)


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
