from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import config
from entities.account import Account
from localization.context import ContextProto


def generate_credentials_text(context: ContextProto, account: Account):
    return context.localize('accounting.credentials') % (config.DOMAIN, account.username, account.password)


def generate_credentials_buttons(context: ContextProto, account: Account, offset: int = None, count: int = 0):
    buttons_matrix = [
        [
            InlineKeyboardButton(context.localize('accounting.change_username'), callback_data=f'username {account.id}'),
            InlineKeyboardButton(context.localize('accounting.reset_password'), callback_data=f'password {account.id}'),
        ],
        [InlineKeyboardButton(context.localize('accounting.delete_account'), callback_data=f'delete {account.id}')],
    ]
    if count > 1:
        _prev = offset - 1 if offset > 0 else count - 1
        _next = offset + 1 if offset < count - 1 else 0
        buttons_matrix.append([
            InlineKeyboardButton('<<', callback_data=f'accounts {_prev}'),
            InlineKeyboardButton('>>', callback_data=f'accounts {_next}'),
        ])
    return InlineKeyboardMarkup(buttons_matrix)
