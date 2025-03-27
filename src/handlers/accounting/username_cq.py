import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

import domain
from handlers.accounting.utils import generate_credentials_buttons, generate_credentials_text
from handlers.filters import has_accounts, username_change
from localization import LocalizedContext
from utils import contact_with_developer

_queue: dict[int:tuple[int, int, int]] = dict()
_access_list: set[int] = set()

pattern = re.compile('^username ([0-9]+)$')
pattern_cancel = re.compile('^username cancel$')


async def handler(update: Update, context: LocalizedContext):
    if not has_accounts.filter(update):
        return

    sender_id = update.callback_query.from_user.id
    account_id = int(context.match.group(1))

    text = context.localize('accounting.enter_username')
    buttons = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(context.localize('common.cancel'), callback_data='username cancel')
    )
    m = await update.effective_message.reply_text(text, reply_markup=buttons)
    _access_list.add(sender_id)
    _queue[sender_id] = account_id, update.effective_message.id, m.id
    await update.callback_query.answer()


async def handler_cancel(update: Update, context: LocalizedContext):
    if not username_change.filter(update):
        return
    query = update.callback_query
    username_change.remove_user(update.effective_user.id)
    if _queue.get(update.effective_user.id) is not None:
        _queue.pop(update.effective_user.id)
    await query.answer(context.localize('common.operation_canceled'))
    await update.effective_message.delete()


async def handler_text(update: Update, context: LocalizedContext):
    username_change.remove_user(update.effective_user.id)
    account_pos, message_id, message_id_2 = _queue.pop(update.effective_user.id)
    username = update.message.text
    result = domain.accounting.change_username(update.effective_user.id, account_pos, username)

    if result.username_exist:
        text = context.localize('accounting.username_exists') % username
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton(context.localize('common.operation_canceled'), callback_data='username cancel')
        ]])
        try:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id_2,
                text=text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            pass  # Ignore message not modified errors
        await update.message.delete()
        username_change.add_user(update.effective_user.id)
        _queue[update.effective_user.id] = account_pos, message_id, message_id_2
        return

    account_info = domain.accounting.get_account(update.effective_user.id, account_pos)
    if account_info.data is None:
        await update.effective_chat.send_message(contact_with_developer(context, action='username'))
        return

    await context.bot.delete_message(update.effective_chat.id, message_id_2)
    await update.message.delete()

    if not result.changed:
        return

    if result.data is None:
        await update.message.reply_text(
            contact_with_developer(
                context,
                action='username',
                id=account_pos,
                raw_text=update.message.text,
            )
        )
        return

    text = generate_credentials_text(context, result.data)
    buttons = generate_credentials_buttons(context, result.data, account_info.offset, account_info.count)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text=text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
    )


def get_handlers():
    return [
        CallbackQueryHandler(handler, pattern),
        CallbackQueryHandler(handler_cancel, pattern_cancel),
        MessageHandler(filters.TEXT & ~filters.COMMAND & username_change, handler_text)
    ]
