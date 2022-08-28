from telethon import Button, TelegramClient

import env
from entities.account import Account


def generate_credentials_text(account: Account, _):
    lines = [
        '**IKEv2**',
        _('__Address__ — `%s`') % env.ADDRESS,
        _('__Username__ — `%s`') % account.username,
        _('__Password__ — `%s`') % account.password
    ]
    return '\n'.join(lines)


def generate_buttons(client: TelegramClient, account: Account, offset: int = None, count: int = 0, _=None):
    buttons_matrix = [
        [Button.inline(_('Change username'), f'username {account.id}')],
        [Button.inline(_('Reset password'), f'password {account.id}')],
        [Button.inline(_('Delete account'), f'delete {account.id}')],
    ]
    if count > 1:
        _prev = offset - 1 if offset > 0 else count - 1
        _next = offset + 1 if offset < count - 1 else 0
        buttons_matrix.append([
            Button.inline('<<', f'accounts {_prev}'),
            Button.inline('>>', f'accounts {_next}'),
        ])
    client.build_reply_markup(buttons_matrix, inline_only=True)
