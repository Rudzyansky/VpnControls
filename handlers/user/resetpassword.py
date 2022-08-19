from telethon.events import register, NewMessage

from handlers.accesslist import users_al


@register(NewMessage(users_al, pattern='/reset'))
async def handler(event: NewMessage.Event):
    pass
