from telegram import Update
from telegram.ext import CommandHandler

from handlers.filters import registered
from handlers.settings.utils import generate_text, generate_buttons
from localization import LocalizedContext


async def handler(update: Update, context: LocalizedContext):
    text = generate_text(context)
    buttons = generate_buttons(context)
    await update.effective_chat.send_message(text, reply_markup=buttons)


def get_handlers():
    return [
        CommandHandler('language', handler, filters=registered)
    ]
