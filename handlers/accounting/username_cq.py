from telethon import Button
from telethon.events import register, CallbackQuery, NewMessage

import domain.accounting
from handlers.accounting.utils import generate_buttons
from localization import translate

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
    _access_list.remove(event.sender_id)
    message_id = _queue.pop(event.sender_id)[2]
    await event.client.delete_messages(event.sender_id, message_id)
    await event.answer(_('Operation canceled'))


@register(NewMessage(_access_list))
@translate()
async def handler_text(event: NewMessage.Event, _):
    _access_list.remove(event.sender_id)
    id, message_id, message_id_2 = _queue.pop(event.sender_id)
    username = event.message.raw_text
    account = domain.accounting.change_username(event.chat_id, id, username)
    await event.client.delete_messages(event.sender_id, message_id_2)
    buttons = generate_buttons(event.client, account, _)
    await event.client.edit_message(event.chat_id, message_id, buttons=buttons)
