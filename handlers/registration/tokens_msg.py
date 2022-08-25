from telethon.events import register, NewMessage
from telethon.utils import get_display_name

from bot_commands.categories import Categories
from domain import registration
from domain.commands import access_list
from localization import translate


@register(NewMessage(access_list(Categories.HAS_TOKENS), pattern='^/tokens$'))
@translate()
async def handler(event: NewMessage.Event, _):
    current_tokens = registration.get_tokens(event.chat_id)
    lines = [_('**List of tokens**'), '']
    for token in current_tokens:
        if token.used_by is None:
            line = _('`%s` __expires in__ **%s**') % (token, token.expire)
        else:
            display_name = get_display_name(await event.client.get_entity(token.used_by))
            line = _('`%s` __expires in__ **%s**, __bound to__ **%s**') % (token, token.expire, display_name)
        lines.append(line)
    await event.client.send_message(event.chat_id, '\n'.join(lines))
