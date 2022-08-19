from telethon.events import register, NewMessage

from handlers.accesslist import admins_al


@register(NewMessage(admins_al, pattern='/register'))
async def register_handler(event: NewMessage.Event):
    pass


handlers = [register_handler]
