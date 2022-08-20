from telethon import Button
from telethon.events import register, InlineQuery
from telethon.tl.types import InputWebDocument, DocumentAttributeImageSize
from telethon.utils import get_display_name

from domain import users
from entities.token import Token
from localization import translate, languages


@register(InlineQuery(users.admins, pattern=r'^invite$'))
@translate(text=False, translations=True)
async def handler(event: InlineQuery.Event, t):
    current_tokens = users.get_current_tokens(event.chat_id)
    articles = []
    lang = users.language(event.chat_id)
    articles += [await invite_article(event, token, lang, t[lang].gettext) for token in current_tokens]
    await event.answer(articles)


@register(InlineQuery(users.admins, pattern=r'^invite/$'))
@translate(text=False, translations=True)
async def handler_space(event: InlineQuery.Event, t):
    current_tokens = users.get_current_tokens(event.chat_id)
    articles = []
    for lang in languages:
        _ = t[lang].gettext
        articles += [await invite_article(event, token, lang, _) for token in current_tokens]
    await event.answer(articles)


@register(InlineQuery(users.admins, pattern=r'^invite/([a-z]{2})$'))
@translate(text=False, translations=True)
async def handler_lang(event: InlineQuery.Event, t):
    lang = event.pattern_match[1]
    if lang not in languages:
        await event.answer()
        return
    current_tokens = users.get_current_tokens(event.chat_id)
    articles = [await invite_article(event, token, lang, t[lang].gettext) for token in current_tokens]
    await event.answer(articles)


@register(InlineQuery(users.admins, pattern=r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})$'))
@translate(text=False, translations=True)
async def handler_token(event: InlineQuery.Event, t):
    token = users.fetch_token(Token(event.pattern_match[1], owner_id=event.chat_id))
    if token is None:
        await event.answer()
    else:
        lang = users.language(event.chat_id)
        await event.answer([await invite_article(event, token, lang, t[lang].gettext)])


@register(InlineQuery(users.admins, pattern=r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})/$'))
@translate(text=False, translations=True)
async def handler_token_space(event: InlineQuery.Event, t):
    token = users.fetch_token(Token(event.pattern_match[1], owner_id=event.chat_id))
    if token is None:
        await event.answer()
    else:
        await event.answer([await invite_article(event, token, lang, t[lang].gettext) for lang in languages])


@register(InlineQuery(users.admins, pattern=r'^invite/([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})/([a-z]{2})$'))
@translate(text=False, translations=True)
async def handler_token_lang(event: InlineQuery.Event, t):
    token = users.fetch_token(Token(event.pattern_match[1], owner_id=event.chat_id))
    if token is None:
        await event.answer()
    else:
        lang = event.pattern_match[2]
        if lang in languages:
            await event.answer([await invite_article(event, token, lang, t[lang].gettext)])
        else:
            await event.answer()


invite_thumb = InputWebDocument('https://false.team/invite128.png', 6105, 'image/png',
                                [DocumentAttributeImageSize(128, 128)])


async def invite_article(event, token, lang, _):
    if token.used_by is None:
        description = ''
    else:
        display_name = get_display_name(await event.client.get_entity(token.used_by))
        description = (_('Bound to %s') % display_name) + ', '
    description += (_('Expires in %s') % token.expire) + '\n' + token.string

    return event.builder.article(_('Invite'), description, thumb=invite_thumb,
                                 text=_('You have been invited to use FalseЪ VPN'), buttons=[
            Button.inline(_('Accept'), b'accept ' + token.bytes + b' ' + lang.encode()),
            Button.inline(_('Decline'), b'decline ' + token.bytes)])
