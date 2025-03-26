from telegram import Update
from telegram.ext import CommandHandler

import domain
from handlers.filters import registered
from localization import LocalizedContext


async def handler(update: Update, context: LocalizedContext):
    await domain.commands.telegram_set_commands(context.chat_id)
    await update.effective_message.delete()


def get_handlers():
    return [
        CommandHandler('refresh', handler, filters=registered)
    ]
