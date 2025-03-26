import re

from telegram import Update
from telegram.constants import ParseMode
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
    account_id = int(context.match.group(1))

    result = domain.accounting.reset_password(update.effective_user.id, account_id)
    if result.data is None:
        await update.effective_message.reply_text(
            text=contact_with_developer(
                context,
                action='password',
                data=update.callback_query.data,
                sender_id=sender_id,
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    if result.changed:
        text = generate_credentials_text(context, result.data)
        buttons = generate_credentials_buttons(context, result.data)
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
