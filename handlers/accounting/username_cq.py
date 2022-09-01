from datetime import datetime

from telethon import Button
from telethon.events import register, CallbackQuery, NewMessage

import domain.accounting
from handlers.accounting.utils import generate_buttons, generate_credentials_text
from localization import translate
from utils import contact_with_developer

_queue: dict[int:tuple[int, int]] = dict()
_access_list: set[int] = set()


@register(CallbackQuery(pattern=rb'^username ([0-9]+)$'))
@translate()
async def handler(event: CallbackQuery.Event, _):
    id = int(event.pattern_match[1])
    text = _('Enter username to change it')
    buttons = event.client.build_reply_markup([
        Button.inline(_('Cancel'), f'username cancel'),
    ], inline_only=True)
    m = await event.client.send_message(event.sender_id, text, buttons=buttons)
    _access_list.add(event.sender_id)
    _queue[event.sender_id] = id, event.message_id, m.id
    await event.answer()


@register(CallbackQuery(pattern=rb'^username cancel$'))
@translate()
async def handler_cancel(event: CallbackQuery.Event, _):
    _access_list.discard(event.sender_id)
    if _queue.get(event.sender_id) is not None:
        _queue.pop(event.sender_id)
    await event.client.delete_messages(event.sender_id, event.message_id)
    await event.answer(_('Operation canceled'))


@register(NewMessage(_access_list, incoming=True))
@translate()
async def handler_text(event: NewMessage.Event, _):
    if event.chat_id not in _access_list:
        return
    _access_list.discard(event.chat_id)
    id, message_id, message_id_2 = _queue.pop(event.chat_id)
    username = event.message.raw_text
    account = domain.accounting.change_username(event.chat_id, id, username)
    if account is not None:
        await event.client.delete_messages(event.sender_id, [message_id_2, event.message.id])
        text = generate_credentials_text(account, _)
        buttons = generate_buttons(event.client, account, _=_)
        await event.client.edit_message(event.chat_id, message_id, text, buttons=buttons)
    else:
        await event.client.send_message(event.sender_id, contact_with_developer(
            _,
            timestamp=datetime.utcnow(),
            action='username',
            id=id,
            raw_text=event.message.raw_text,
            chat_id=event.chat_id,
        ))
