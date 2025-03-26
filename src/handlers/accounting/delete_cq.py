import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.filters import has_accounts
from localization import LocalizedContext

pattern = re.compile('^delete ([0-9]+)$')


async def handler(update: Update, context: LocalizedContext):
    if not has_accounts.filter(update):
        return
    await update.callback_query.answer()
    await update.effective_message.reply_text(context.localize('accounting.delete_success'))

    sender_id = update.callback_query.from_user.id
    position = int(context.match.group(1))

    if await domain.accounting.delete_account(sender_id, position):
        await update.effective_message.edit_text(context.localize('accounting.delete_success'))
    else:
        await update.effective_message.edit_text(context.localize('accounting.delete_fail'))


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
