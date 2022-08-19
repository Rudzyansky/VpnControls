from telethon.events import register, NewMessage

from handlers.accesslist import users_al


@register(NewMessage(users_al, pattern='/acquire'))
async def handler(event: NewMessage.Event):
    # id = event.chat.id
    #
    # if not users.is_registered(id):
    #     await event.message.reply('You are not registered. Contact with administrator.')
    #     return
    #
    # username = accounts.get_username(id)
    # if username is None:
    #     _un = event.chat.username
    #     _fn = event.chat.first_name
    #     _ln = event.chat.last_name  # (maybe None)
    #     username = _fn if _un is None else _un
    #
    # controls.add_user(username)
    pass
