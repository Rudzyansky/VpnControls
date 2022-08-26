from telethon import TelegramClient, Button
from telethon.events import register, CallbackQuery
from telethon.utils import get_display_name

from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from localization import translate


@register(CallbackQuery(access_list(Categories.HAS_ACTUAL_TOKENS), pattern=rb'^next ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    text, buttons = await text_and_buttons(event.client, _, event.chat_id, int(event.pattern_match[1]))
    await event.edit(text, buttons=buttons)


async def text_and_buttons(client: TelegramClient, _, user_id: int, offset: int = 0):
    offset, token, count = registration.get_next_actual_token(user_id, offset)
    if count == 0 or token is None:
        return _('No tokens found'), None

    if token.used_by is None:
        text = _('Token `%s`\n__Expires in__ **%s**') % (token, token.expire)
    else:
        display_name = get_display_name(await client.get_entity(token.used_by))
        text = _('Token `%s`\n__Expires in__ **%s**\n__Bound to__ **%s**') % (token, token.expire, display_name)

    # [   Invite   ]   [  Revoke   ]
    # [ Invite in another language ]
    # [         Next token         ]
    buttons_matrix = [
        [
            Button.switch_inline(_('Invite'), f'invite/{token}', same_peer=False),
            Button.inline(_('Revoke'), b'revoke ' + token.bytes)
        ],
        [Button.switch_inline(_('Invite in another language'), f'invite/{token}/', same_peer=False)],
    ]
    if count > 1:
        buttons_matrix.append([Button.inline(_('Next token (%d of %d)') % (offset + 1, count), f'next {offset + 1}')])
    buttons = client.build_reply_markup(buttons_matrix, inline_only=True)

    return text, buttons
