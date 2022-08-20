from datetime import datetime

from telethon import Button
from telethon.events import register, NewMessage

import utils
from domain import users
from entities.token import Token
from localization import translate


@register(NewMessage(users.admins, pattern='/register'))
@translate
async def handler(event: NewMessage.Event, _, _n):
    limit = 2

    current_tokens = tokens.get_all(event.chat_id)
    if len(current_tokens) >= limit:
        lines = [_n('Unable to issue token. __The limit of **%d** invitation per week has been reached.__',
                    'Unable to issue token. __The limit of **%d** invitations per week has been reached.__',
                    limit) % limit,
                 '']
        for token in current_tokens:
            if token.used_by is None:
                line = _('`%s` __expires in__ **%s**') % (token, token.expire)
            else:
                line = _('__slot will be reset in__ **%s**') % token.expire
            lines.append(line)
        await event.client.send_message(event.chat_id, '\n'.join(lines))
        return

    token = tokens.add(Token(owner_id=event.chat_id))

    if token is None:
        payload = utils.debug_payload(user_id=event.chat_id, timestamp=datetime.utcnow())
        text = _('Something went wrong. Contact the developer') + '\n\n' + payload
        await event.reply(text)
        return

    text = _('Token `%s` issued\n__Expires in__ **%s**') % (token, token.expire)
    await event.client.send_message(event.chat_id, text,
                                    buttons=[Button.switch_inline(_('Invite'), f'invite {token}', same_peer=False),
                                             Button.inline(_('Revoke'), b'revoke ' + token.bytes)])
