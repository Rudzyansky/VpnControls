import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.accounting.utils import generate_credentials_buttons, generate_credentials_text
from handlers.filters import has_accounts
from localization import LocalizedContext
from utils import contact_with_developer

pattern = re.compile('^password ([0-9]+)$')


async def handler(update: Update, context: LocalizedContext):
    if not has_accounts.filter(update):
        return

    sender_id = update.callback_query.from_user.id
    position = int(context.match.group(1))

    account_info = domain.accounting.get_account(update.effective_user.id, position)
    if account_info.data is None:
        await update.effective_chat.send_message(contact_with_developer(context, action='password'))
        return

    result = domain.accounting.reset_password(update.effective_user.id, position)
    if result.data is None:
        await update.effective_message.reply_text(
            contact_with_developer(
                context,
                action='password',
                data=update.callback_query.data,
                sender_id=sender_id,
            )
        )
        return

    if result.changed:
        text = generate_credentials_text(context, result.data)
        buttons = generate_credentials_buttons(context, result.data, account_info.offset, account_info.count)
        try:
            await update.effective_message.edit_text(text, reply_markup=buttons)
        except Exception:
            pass  # Ignore message not modified errors
    else:
        await update.callback_query.answer()


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
