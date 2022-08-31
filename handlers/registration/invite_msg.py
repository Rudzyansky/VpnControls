from telethon.events import register, NewMessage

from bot_commands.categories import Categories
from domain.commands import access_list
from localization import translate
from .invite_cq import text_and_buttons


@register(NewMessage(access_list(Categories.HAS_TOKENS), pattern='^/invite$'))
@translate()
async def handler(event: NewMessage.Event, _):
    text, buttons = await text_and_buttons(event.client, _, event.chat_id)
    await event.client.send_message(event.chat_id, text, buttons=buttons)
