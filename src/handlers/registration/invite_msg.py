from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler

import domain
from handlers.filters import can_invite
from handlers.registration.utils import generate_invite_text, generate_buttons
from localization import LocalizedContext


async def handler(update: Update, context: LocalizedContext):
    offset, count, token = domain.registration.get_actual_token(context.chat_id)
    text = generate_invite_text(context, token, count)
    buttons = generate_buttons(context, token, offset, count) if token is not None else None
    await update.effective_chat.send_message(text=text, reply_markup=buttons, parse_mode=ParseMode.HTML)


def get_handlers():
    return [
        CommandHandler('invite', handler, filters=can_invite)
    ]
