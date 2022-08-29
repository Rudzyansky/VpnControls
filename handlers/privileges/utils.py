from typing import Optional

from telethon import Button, TelegramClient

from domain.entities.users_meta import UsersMeta


def generate_users_message(client: TelegramClient, data: UsersMeta, _) -> tuple[str, Optional[list[list[Button]]]]:
    if data.pages_count == 0:
        return _('No users found'), None
    buttons_matrix = []
    for user in data.users:
        buttons_matrix.append([Button.inline(user.display_name, f'user {user.id}')])
    if data.pages_count > 1:
        _prev = data.page - 1 if data.page > 1 else data.pages_count
        _next = data.page + 1 if data.page < data.pages_count else 1
        buttons_matrix.append([
            Button.inline('<<', f'users {_prev}'),
            Button.inline('>>', f'users {_next}'),
        ])
    text = _('Choose user from list below:')
    buttons = client.build_reply_markup(buttons_matrix, inline_only=True)
    return text, buttons


def generate_user_message(client: TelegramClient, data, _) -> tuple[str, Optional[list[list[Button]]]]:
    text = '\n'.join([
        _('[**%s**](tg://user?id=%s)') % (data.user.display_name, data.user.id),
        _('__Accounts limit__ — `%s`') % data.user.accounts_limit,
        _('__Accounts__ — `%s`') % data.user.accounts_count,
        _('__Tokens limit__ — `%s`') % data.user.tokens_limit,
        _('__Users__ — `%s`') % data.user.users_count,
    ])
    buttons_matrix = list()
    if data.user.accounts_count > 0:
        buttons_matrix.append([
            Button.inline(_('View accounts'), f'accounts view {data.user.id}'),
            Button.inline(_('Remove all accounts'), f'accounts remove {data.user.id}'),
        ])
    buttons_matrix.append([
        Button.inline(_('Accounts limit'), ''),
        Button.inline(_('Tokens limit'), ''),
    ])
    buttons_matrix.append([
        Button.inline(_('Transfer to another administrator'), ''),
    ])
    buttons_matrix.append([
        Button.inline(_('Revoke'), ''),
        Button.inline(_('Remove'), ''),
    ])
    # [    View accounts    ][ Remove all accounts ]
    # [   Accounts limit    ][    Tokens limit     ]
    # [     Transfer to another administrator      ]
    # [       Revoke        ][       Remove        ]
    # [              << Back to menu               ]

    for user in data.users:
        buttons_matrix.append([Button.inline(user.display_name, f'user {user.id}')])

    buttons_matrix.append([Button.inline(_('<< Back to menu'), f'users {data.page}')])

    buttons = client.build_reply_markup(buttons_matrix, inline_only=True)
    return text, buttons
