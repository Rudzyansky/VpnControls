import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler

import domain
from handlers.filters import can_register
from localization import LocalizedContext
from utils import contact_with_developer

pattern = re.compile(r'^accept (.{16}) ([a-z]{2})$')


async def handler(update: Update, context: LocalizedContext):
    if not can_register.filter(update):
        return
    await update.callback_query.answer()
    await update.effective_message.reply_text(context.localize('registration.accept_success'))

    token_str = context.match.group(1)
    lang = context.match.group(2)
    sender_id = update.callback_query.from_user.id
    token = domain.registration.get_token(token_str)

    if token is None or (token.used_by is not None and token.used_by != sender_id):
        await update.effective_message.edit_text(context.localize('registration.invitation_invalid', lang))
    token.used_by = sender_id
    if domain.registration.use_token(token):
        await update.callback_query.answer(url=f'https://t.me/{context.bot.username}?start={lang}')
    else:
        await update.callback_query.answer(context.localize('common.error_occurred', lang))
        await update.effective_chat.send_message(
            text=contact_with_developer(
                context,
                action='accept',
                sender_id=sender_id,
            ),
            parse_mode=ParseMode.HTML,
        )


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
