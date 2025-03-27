import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler

import domain
from handlers.accounting.utils import generate_credentials_text, generate_credentials_buttons
from handlers.filters import can_create_account
from localization import LocalizedContext
from utils import contact_with_developer


async def handler(update: Update, context: LocalizedContext):
    username = update.effective_chat.username or update.effective_chat.full_name

    try:
        account = await domain.accounting.create_account(update.effective_chat.id, username)
        if account is not None:
            text = generate_credentials_text(context, account)
            buttons = generate_credentials_buttons(context, account)
            await update.effective_chat.send_message(text, reply_markup=buttons)
        else:
            await update.effective_chat.send_message(
                contact_with_developer(context, action='acquire', username=username)
            )
    except Exception as e:
        logging.error(e, exc_info=True)
        await update.effective_chat.send_message(
            contact_with_developer(context, action='acquire', username=username)
        )


def get_handlers():
    return [
        CommandHandler('acquire', handler, filters=can_create_account)
    ]
