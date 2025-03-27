from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from entities.token import Token
from localization.context import ContextProto


def generate_invite_text(context: ContextProto, token: Token, count=1):
    if count == 0 or token is None:
        return context.localize('registration.token_info_no_tokens')
    elif token.used_by is None:
        return context.localize('registration.token_info_expires') % (token, token.expire)
    else:
        return context.localize('registration.token_info_expires_bounded') % (token, token.expire, token.used_by)


def generate_buttons(context: ContextProto, token: Token, offset: int = None, count: int = 1):
    buttons_matrix = [
        [
            InlineKeyboardButton(context.localize('registration.invite'), callback_data=f'invite {token}'),
            InlineKeyboardButton(context.localize('registration.revoke'), callback_data=f'revoke {token}'),
        ],
        [InlineKeyboardButton(context.localize('registration.invite_in_another_language'),
                              callback_data=f'invite {token}/')],
    ]
    if count > 1:
        _prev = offset - 1 if offset > 0 else count - 1
        _next = offset + 1 if offset < count - 1 else 0
        buttons_matrix.append([
            InlineKeyboardButton('<<', callback_data=f'invite {_prev}'),
            InlineKeyboardButton('>>', callback_data=f'invite {_next}'),
        ])
    return InlineKeyboardMarkup(buttons_matrix)
