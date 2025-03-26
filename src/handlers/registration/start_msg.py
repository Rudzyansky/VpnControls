from telegram import Update
from telegram.ext import CommandHandler

import domain
from handlers.filters import can_register, registered
from localization import LocalizedContext


async def handler(update: Update, context: LocalizedContext):
    args = update.effective_message.text.split()[1:]
    lang = args[0] if args else 'en'
    user = await domain.registration.register_user(context.chat_id, lang)
    if user is None:
        await update.effective_chat.send_message(context.localize('errors.contact_developer', lang))
        return


def get_handlers():
    return [
        CommandHandler('start', handler, filters=can_register | registered)
    ]
