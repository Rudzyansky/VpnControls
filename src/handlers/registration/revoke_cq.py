import re

from telegram import Update
from telegram.ext import CallbackQueryHandler

import domain
from handlers.filters import can_invite
from localization import LocalizedContext

pattern = re.compile(r'^revoke (.{16})$')


async def handler(update: Update, context: LocalizedContext):
    if not can_invite.filter(update):
        return

    token = context.match.group(1)

    if await domain.registration.revoke_token(token, context.chat_id):
        await update.effective_message.edit_text(context.localize('registration.invitation_revoked'))
    else:
        await update.effective_message.edit_text(context.localize('registration.invitation_invalid'))


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern)
    ]
