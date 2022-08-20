from telethon import Button
from telethon.events import register, InlineQuery
from telethon.tl.types import InputWebDocument, DocumentAttributeImageSize
from telethon.utils import get_display_name

from domain import users
from entities.token import Token
from localization import translate


@register(InlineQuery(users.admins, pattern=r'^invite$'))
@translate
async def handler_all(event: InlineQuery.Event, _):
    current_tokens = users.get_tokens(event.chat_id)
    current_tokens = filter(lambda token: token.used_by != token.owner_id, current_tokens)
    articles = [await invite_article(event, token, _) for token in current_tokens]
    await event.answer(articles)


@register(InlineQuery(users.admins, pattern=r'^invite ([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})$'))
@translate
async def handler_one(event: InlineQuery.Event, _):
    start, end = event.pattern_match.regs[1]
    token = users.get_token(Token(event.text[start:end], owner_id=event.chat_id))
    if token is None:
        await event.answer()
    else:
        await event.answer([await invite_article(event, token, _)])


invite_thumb = InputWebDocument('https://false.team/invite128.png', 6105, 'image/png',
                                [DocumentAttributeImageSize(128, 128)])


async def invite_article(event, token, _):
    display_name = get_display_name(await event.client.get_entity(token.used_by))

    description = '' if token.used_by is None else (_('Bound to %s') % display_name) + ', '
    description += (_('Expires in %s') % token.expire) + '\n' + token

    return event.builder.article(_('Invite'), description, thumb=invite_thumb,
                                 text=_('You have been invited to use FalseЪ VPN'),
                                 buttons=[Button.inline(_('Accept'), b'accept ' + token.bytes),
                                          Button.inline(_('Decline'), b'decline ' + token.bytes)])
