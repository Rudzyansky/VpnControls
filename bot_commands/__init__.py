from telethon.tl.functions.bots import ResetBotCommandsRequest, SetBotCommandsRequest
from telethon.tl.types import BotCommandScopeDefault, BotCommandScopePeer
from telethon.utils import get_input_peer

from domain import users
from localization import languages
from .commands import commands_user, commands_admin


async def setup(client):  # todo переделать архитектуру: изменение меню по запросу
    for lang_code in languages:
        await client(ResetBotCommandsRequest(
            scope=BotCommandScopeDefault(), lang_code=lang_code))

    for user_id in users.registered - users.admins:
        user = await client.get_entity(user_id)
        lang_code = users.language(user_id)
        await client(SetBotCommandsRequest(
            scope=BotCommandScopePeer(get_input_peer(user)),
            lang_code=lang_code, commands=commands_user[lang_code]))

    for user_id in users.admins:
        user = await client.get_entity(user_id)
        lang_code = users.language(user_id)
        await client(SetBotCommandsRequest(
            scope=BotCommandScopePeer(get_input_peer(user)),
            lang_code=lang_code, commands=commands_admin[lang_code]))


__all__ = [
    'setup'
]
