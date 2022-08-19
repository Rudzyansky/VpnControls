from telethon.events import register, NewMessage

from handlers.accesslist import users_al


@register(NewMessage(users_al, pattern='/username'))
async def handler(event: NewMessage.Event):
    pass
