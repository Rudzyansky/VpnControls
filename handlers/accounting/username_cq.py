from datetime import datetime

from telethon import Button
from telethon.errors import MessageNotModifiedError
from telethon.events import register, CallbackQuery, NewMessage

import domain.accounting
from bot_commands.categories import Categories
from domain.commands import access_list
from handlers.accounting.utils import generate_buttons, generate_credentials_text
from localization import translate
from utils import contact_with_developer

_queue: dict[int:tuple[int, int]] = dict()
_access_list: set[int] = set()


def handler_filter(event: CallbackQuery.Event):
    return event.sender_id in access_list(Categories.HAS_ACCOUNTS)


@register(CallbackQuery(func=handler_filter, pattern=rb'^username ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    _id = int(event.pattern_match[1])
    text = _('Enter username to change it')
    buttons = event.client.build_reply_markup([
        Button.inline(_('Cancel'), f'username cancel'),
    ], inline_only=True)
    m = await event.reply(text, buttons=buttons)
    _access_list.add(event.sender_id)
    _queue[event.sender_id] = _id, event.message_id, m.id
    await event.answer()


def handler_cancel_filter(event: CallbackQuery.Event):
    return event.sender_id in _access_list


@register(CallbackQuery(func=handler_cancel_filter, pattern=rb'^username cancel$'))
@translate()
async def handler_cancel(event: CallbackQuery.Event, _):
    _access_list.discard(event.sender_id)
    if _queue.get(event.sender_id) is not None:
        _queue.pop(event.sender_id)
    await event.answer(_('Operation canceled'))
    await event.client.delete_messages(event.sender_id, event.message_id)


def handler_text_filter(event: CallbackQuery.Event):
    return event.chat_id in _access_list


@register(NewMessage(func=handler_text_filter, incoming=True))
@translate()
async def handler_text(event: NewMessage.Event, _):
    _access_list.discard(event.chat_id)
    id, message_id, message_id_2 = _queue.pop(event.chat_id)
    username = event.message.raw_text
    result = domain.accounting.change_username(event.chat_id, id, username)

    if result.username_exist:
        text = _('Username `%s` already exist. Enter another username to change it') % username
        buttons = event.client.build_reply_markup([Button.inline(_('Cancel'), f'username cancel')], inline_only=True)
        try:
            await event.client.edit_message(event.chat_id, message_id_2, text, buttons=buttons)
        except MessageNotModifiedError:
            pass
        await event.client.delete_messages(event.sender_id, event.message.id)
        _access_list.add(event.chat_id)
        _queue[event.chat_id] = id, message_id, message_id_2
        return

    await event.client.delete_messages(event.sender_id, [message_id_2, event.message.id])

    if not result.changed:
        return

    if result.data is None:
        await event.client.send_message(event.sender_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='username',
            id=id,
            raw_text=event.message.raw_text,
            chat_id=event.chat_id,
        ))
        return

    text = generate_credentials_text(result.data, _)
    buttons = generate_buttons(event.client, result.data, _=_)
    await event.client.edit_message(event.chat_id, message_id, text, buttons=buttons)
