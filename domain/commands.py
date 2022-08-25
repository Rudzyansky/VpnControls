from telethon.tl.functions.bots import SetBotCommandsRequest, ResetBotCommandsRequest
from telethon.tl.types import BotCommand, BotCommandScopePeer
from telethon.utils import get_input_peer

import bot_commands
import database
from bot_commands.categories import Categories
from domain import common
from entities.user import User

_cache: dict[int:list[BotCommand]] = dict()
_cache_categories: dict[int:set[Categories]] = dict()
_access_lists = {c: set() for c in Categories}


def _recalculate_cache(user: User):
    _cache[user.id] = bot_commands.get(user.language, *_cache_categories[user.id])


def _recalculate_access_lists(user: User):
    single: set[int] = {user.id}
    for cmd in set(Categories) - user.commands:
        _access_lists[cmd] -= single
    for cmd in user.commands:
        _access_lists[cmd] += single


for __user in database.common.get_all_users():
    _cache_categories[__user.id] = __user.commands
    _recalculate_cache(__user)
    _recalculate_access_lists(__user)


def access_list(*categories: Categories) -> set[int]:
    result = set()
    for category in categories:
        result |= _access_lists.get(category)
    return result


async def _telegram_reset_commands(user: User):
    scope = BotCommandScopePeer(get_input_peer(await common.client.get_entity(user.id)))
    await common.client(ResetBotCommandsRequest(scope, user.language))


async def _telegram_set_commands(user: User):
    scope = BotCommandScopePeer(get_input_peer(await common.client.get_entity(user.id)))
    await common.client(SetBotCommandsRequest(scope, user.language, _cache[user.id]))


def _set_user_commands_db(user: User):
    database.common.set_user_commands(user.id, user.commands_int)


async def refresh_commands(user: User):
    await _telegram_set_commands(user)


async def _update(user: User):
    _recalculate_cache(user)
    _recalculate_access_lists(user)
    _set_user_commands_db(user)
    await _telegram_set_commands(user)


async def set_categories(user: User, *categories: Categories):
    _cache_categories[user.id] = set(categories)
    await _update(user)


async def add_categories(user: User, *categories: Categories):
    _cache_categories[user.id] += set(categories)
    await _update(user)


async def remove_categories(user: User, *categories: Categories):
    _cache_categories[user.id] -= set(categories)
    await _update(user)
