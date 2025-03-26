from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler

import domain
from handlers.filters import has_tokens
from localization import LocalizedContext


async def handler(update: Update, context: LocalizedContext):
    current_tokens = domain.registration.get_tokens(context.chat_id)
    lines = [context.localize('registration.list_of_tokens'), '']
    for token in current_tokens:
        if token.used_by is None:
            line = context.localize('registration.token_expires_in') % (token, token.expire)
        else:
            if token.used_by == context.chat_id:
                line = context.localize('registration.token_revoked') % (token, token.expire)
            else:
                display_name = f'<a href="tg://resolve?id={token.used_by}">{token.used_by}</a>'
                line = context.localize('registration.token_bound_to') % (token, token.expire, display_name)
        lines.append(line)
    await update.effective_chat.send_message('\n'.join(lines), parse_mode=ParseMode.HTML)


def get_handlers():
    return [
        CommandHandler('tokens', handler, filters=has_tokens)
    ]
