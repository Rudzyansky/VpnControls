from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler

import domain
from handlers.accounting.utils import generate_credentials_buttons, generate_credentials_text
from handlers.filters import has_accounts
from localization import LocalizedContext
from utils import contact_with_developer


async def handler(update: Update, context: LocalizedContext):
    result = domain.accounting.get_account(update.effective_chat.id, 0)
    if result.data is None:
        await update.effective_chat.send_message(contact_with_developer(context, action='accounts'))
        return

    text = generate_credentials_text(context, result.data)
    keyboard = generate_credentials_buttons(context, result.data, result.offset, result.count)
    await update.message.reply_text(text, reply_markup=keyboard)


def get_handlers():
    return [
        CommandHandler('accounts', handler, filters=has_accounts)
    ]
