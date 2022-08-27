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


def generate_buttons(client: TelegramClient, account: Account, _):
    client.build_reply_markup([
        Button.inline(_('Change username'), f'username {account.id}'),
        Button.inline(_('Reset password'), f'password {account.id}'),
        Button.inline(_('Delete account'), f'delete {account.id}'),
    ], inline_only=True)
