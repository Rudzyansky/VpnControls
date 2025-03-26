import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.filters import can_register
from localization import LocalizedContext

pattern = re.compile(r'^decline (.{16}) ([a-z]{2})$')


async def handler(update: Update, context: LocalizedContext):
    if not can_register.filter(update):
        return

    token = context.match.group(1)
    lang = context.match.group(2)

    if await domain.registration.revoke_token_force(token):
        await update.effective_message.edit_text(context.localize('registration.invitation_revoked', lang))
    else:
        await update.effective_message.edit_text(context.localize('registration.invitation_invalid', lang))


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
