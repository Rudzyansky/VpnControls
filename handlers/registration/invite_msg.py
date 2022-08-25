from telethon import Button
from telethon.events import register, NewMessage
from telethon.utils import get_display_name

from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from localization import translate


@register(NewMessage(access_list(Categories.HAS_TOKENS), pattern='^/invite$'))
@translate()
async def handler(event: NewMessage.Event, _):
    current_tokens = registration.get_tokens(event.chat_id)
    for token in current_tokens:
        if token.used_by is None:
            text = _('Token `%s`\n__Expires in__ **%s**') % (token, token.expire)
        else:
            display_name = get_display_name(await event.client.get_entity(token.used_by))
            text = _('Token `%s`\n__Expires in__ **%s**\n__Bound to__ **%s**') % (token, token.expire, display_name)
        buttons = event.client.build_reply_markup([
            [
                Button.switch_inline(_('Invite'), f'invite/{token}', same_peer=False),
                Button.inline(_('Revoke'), b'revoke ' + token.bytes)
            ],
            [Button.switch_inline(_('Invite in another language'), f'invite/{token}/', same_peer=False)]
        ], inline_only=True)
        await event.client.send_message(event.chat_id, text, buttons=buttons)
