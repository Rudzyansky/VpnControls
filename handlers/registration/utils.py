from telethon import TelegramClient, Button
from telethon.utils import get_display_name

from entities.token import Token


def generate_issue_text(token: Token, _):
    return _('Token `%s` issued\n__Expires in__ **%s**') % (token, token.expire)


async def generate_invite_text(client: TelegramClient, token: Token, count=1, _=None):
    if count == 0 or token is None:
        return _('No tokens found')
    elif token.used_by is None:
        return _('Token `%s`\n__Expires in__ **%s**') % (token, token.expire)
    else:
        display_name = get_display_name(await client.get_entity(token.used_by))
        return _('Token `%s`\n__Expires in__ **%s**\n__Bound to__ **%s**') % (token, token.expire, display_name)


def generate_buttons(client: TelegramClient, token: Token, offset: int = None, count: int = 1, _=None):
    buttons_matrix = [
        [
            Button.switch_inline(_('Invite'), f'invite/{token}', same_peer=False),
            Button.inline(_('Revoke'), b'revoke ' + token.bytes),
        ],
        [Button.switch_inline(_('Invite in another language'), f'invite/{token}/', same_peer=False)],
    ]
    if count > 1:
        _prev = offset - 1 if offset > 0 else count - 1
        _next = offset + 1 if offset < count - 1 else 0
        buttons_matrix.append([
            Button.inline('<<', f'invite {_prev}'),
            Button.inline('>>', f'invite {_next}'),
        ])
    return client.build_reply_markup(buttons_matrix, inline_only=True)
