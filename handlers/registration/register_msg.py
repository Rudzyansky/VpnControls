from datetime import datetime

from telethon import Button
from telethon.events import register, NewMessage

import utils
from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from localization import translate


@register(NewMessage(access_list(Categories.CAN_ISSUE_TOKEN), pattern='^/register$'))
@translate(current=True)
async def handler(event: NewMessage.Event, _, t):
    limit = registration.get_tokens_limit(event.chat_id)

    current_tokens = registration.get_tokens(event.chat_id)
    if len(current_tokens) >= limit:
        lines = [t.ngettext(
            'Unable to issue token\n__The limit of **%d** invitation per week has been reached__',
            'Unable to issue token\n__The limit of **%d** invitations per week has been reached__',
            limit) % limit, '']
        for token in current_tokens:
            if token.used_by is None:
                line = _('`%s` __expires in__ **%s**') % (token, token.expire)
            else:
                line = _('__slot will be reset in__ **%s**') % token.expire
            lines.append(line)
        await event.client.send_message(event.chat_id, '\n'.join(lines))
        return

    token = registration.create_token(event.chat_id)

    if token is None:
        payload = utils.debug_payload(user_id=event.chat_id, timestamp=datetime.utcnow())
        text = _('Something went wrong. Contact the developer') + '\n\n' + payload
        await event.reply(text)
        return

    text = _('Token `%s` issued\n__Expires in__ **%s**') % (token, token.expire)
    buttons = event.client.build_reply_markup([
        [
            Button.switch_inline(_('Invite'), f'invite/{token}', same_peer=False),
            Button.inline(_('Revoke'), b'revoke ' + token.bytes)
        ],
        [Button.switch_inline(_('Invite in another language'), f'invite/{token}/', same_peer=False)]
    ], inline_only=True)
    await event.client.send_message(event.chat_id, text, buttons=buttons)
