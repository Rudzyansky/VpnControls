from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler

import domain
from handlers.filters import can_issue_token
from handlers.registration.utils import generate_buttons
from localization import LocalizedContext
from utils import contact_with_developer


async def handler(update: Update, context: LocalizedContext):
    token = await domain.registration.create_token(context.chat_id)
    if token is not None:
        text = context.localize('registration.token_issued') % (token, token.expire)
        buttons = generate_buttons(context, token)
        await update.effective_chat.send_message(text=text, reply_markup=buttons, parse_mode=ParseMode.HTML)
    else:
        await update.effective_message.reply_text(contact_with_developer(context, action='issue token'))


def get_handlers():
    return [
        CommandHandler('issue', handler, filters=can_issue_token)
    ]
