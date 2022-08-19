import datetime

from telethon import Button
from telethon.events import register, NewMessage, InlineQuery, CallbackQuery
from telethon.tl.types import InputWebDocument, DocumentAttributeImageSize
from telethon.utils import get_display_name

import utils
from database import users, tokens
from handlers.accesslist import admins_al, users_al
from handlers.token import Token


async def assigned_display_name(client, token):
    return get_display_name(await client.get_entity(token.used_by))


@register(NewMessage(admins_al, pattern='/register'))
async def register_handler(event: NewMessage.Event):
    limit = 2

    current_tokens = tokens.get_all(event.chat_id)
    if len(current_tokens) >= limit:
        payload = '\n'.join([f'__slot will be reset in__ **{t.expire}**' if t.used_by else
                             f'`{t}` __expires in__ **{t.expire}**' for t in current_tokens])
        text = 'Unable to issue token. ' \
               f'__The limit of__ **{limit}** __invitations per week has been reached.__\n\n' + payload
        await event.client.send_message(event.chat_id, text)
        return

    token = tokens.add(Token(owner_id=event.chat_id))

    if token is None:
        payload = utils.debug_payload(user_id=event.chat_id, timestamp=datetime.datetime.utcnow())
        text = 'Something went wrong. Contact the developer\n\n' + payload
        await event.reply(text)
        return

    await event.client.send_message(event.chat_id, f'Token `{token}` issued\n__Expires in__ **{token.expire}**',
                                    buttons=[Button.switch_inline('Invite', f'invite {token}', same_peer=False),
                                             Button.inline('Revoke', b'revoke ' + token.bytes)])


invite_thumb = InputWebDocument('https://false.team/invite128.png', 6105, 'image/png',
                                [DocumentAttributeImageSize(128, 128)])


async def invite_article(event, token):
    used_by = '' if token.used_by is None else \
        f'Bound to {get_display_name(await event.client.get_entity(token.used_by))}, '
    expire = f'Expires in {token.expire}'
    return event.builder.article(title='Invite', thumb=invite_thumb,
                                 description=f'{used_by}{expire}\n{token}',
                                 text='You have been invited to use FalseЪ VPN',
                                 buttons=[Button.inline('Accept', b'accept ' + token.bytes),
                                          Button.inline('Decline', b'decline ' + token.bytes)])


@register(InlineQuery(admins_al, pattern=r'^invite$'))
async def invite_all_handler(event: InlineQuery.Event):
    current_tokens = tokens.get_all(event.chat_id)
    current_tokens = filter(lambda t: t.used_by != t.owner_id, current_tokens)
    articles = [await invite_article(event, t) for t in current_tokens]
    await event.answer(articles)


@register(InlineQuery(admins_al, pattern=r'^invite ([0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12})$'))
async def invite_one_handler(event: InlineQuery.Event):
    start, end = event.pattern_match.regs[1]
    token = tokens.get(Token(event.text[start:end], owner_id=event.chat_id))
    if token is None:
        await event.answer()
    else:
        await event.answer([await invite_article(event, token)])


@register(CallbackQuery(pattern=rb'^accept (.{16})$'))
async def callback_accept_handler(event: CallbackQuery.Event):
    if event.sender_id in users_al:
        await event.answer('Access denied')
        return

    _un = (await event.client.get_me()).username
    start, end = event.data_match.regs[1]
    token = tokens.get(Token(event.data[start:end], owner_id=event.chat_id))
    if token is None or (token.used_by is not None and token.used_by != event.sender_id):
        await event.edit('Invitation is invalid')
        return

    token.used_by = event.sender_id
    if tokens.use(token):
        await event.answer(url=f'https://t.me/{_un}?start={token}')
        # await event.edit('Invitation turned into a pumpkin')
    else:
        await event.answer('An error has occurred. Please contact your administrator')
        payload = utils.debug_payload(chat_id=event.chat_id, sender_id=event.sender_id,
                                      timestamp=datetime.datetime.utcnow())
        text = 'Something went wrong. Contact the developer\n\n' + payload
        await event.client.send_message(event.chat_id, text)


@register(CallbackQuery(pattern=rb'^decline (.{16})$'))
async def callback_decline_handler(event: CallbackQuery.Event):
    if event.sender_id in users_al:
        await event.answer('Access denied')
        return

    start, end = event.data_match.regs[1]
    if tokens.revoke(Token(event.data[start:end], owner_id=event.chat_id)):
        await event.edit('Invitation turned into a pumpkin')
    else:
        await event.edit('Invitation is invalid')


@register(CallbackQuery(pattern=rb'^revoke (.{16})$'))
async def callback_revoke_handler(event: CallbackQuery.Event):
    if event.sender_id not in admins_al:
        await event.answer('Access denied')
        return

    start, end = event.data_match.regs[1]
    if tokens.revoke(Token(event.data[start:end], owner_id=event.chat_id)):
        await event.edit('Invitation turned into a pumpkin')
    else:
        await event.edit('Invitation is invalid')


@register(NewMessage(users_al, blacklist_chats=True, pattern=rf'^/start$'))
async def start_handler(event: NewMessage.Event):
    if not tokens.check_user(event.chat_id):
        return
    users.add_user(event.chat_id)
    # todo say hello


handlers = [register_handler,
            invite_all_handler,
            invite_one_handler,
            callback_accept_handler,
            callback_decline_handler,
            callback_revoke_handler,
            start_handler]
