from telethon.events import register, NewMessage

from handlers.accesslist import admins_al


@register(NewMessage(admins_al, pattern='/unregister'))
async def handler(event: NewMessage.Event):
    pass
