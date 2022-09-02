from functools import reduce

from telethon.tl.functions.bots import SetBotCommandsRequest
from telethon.tl.types import BotCommandScopePeer
from telethon.utils import get_input_peer

import bot_commands
import database
import domain.common
from bot_commands.categories import Categories
from database.abstract import Connection
from domain import common
from domain.types import *

# Declarations

_categories: CategoriesCache = CategoriesCache()
_commands: CommandsCache = CommandsCache()
_access_lists: AccessListsCache = AccessListsCache()


# Access lists cache

def access_list(category: Categories):
    return _access_lists[category]


# Commands cache

async def update(user_id: int, append: set[Categories] = None, remove: set[Categories] = None, c=None):
    if append is None:
        append = set()
    if remove is None:
        remove = set()

    previous = _categories[user_id]
    append.difference_update(previous)
    remove.intersection_update(previous)

    # No updates
    if len(append) + len(remove) == 0:
        return

    # Categories cache
    _categories.add(user_id, append)
    _categories.remove(user_id, remove)
    current = _categories[user_id]

    # Database
    current_int = reduce(lambda a, b: a | b, current).conjugate() if len(current) > 0 else 0
    database.commands.set_user_commands(user_id, current_int, c=c)

    # Commands cache
    _commands[user_id] = bot_commands.get(domain.common.language(user_id), current)

    # Access lists cache
    for category in append:
        _access_lists.add(category, {user_id})
    for category in remove:
        _access_lists.remove(category, {user_id})

    # Telegram update
    await telegram_set_commands(user_id)


# Commands

def recalculate_commands(user_id: int):
    _commands[user_id] = bot_commands.get(domain.common.language(user_id), _categories[user_id])


# Telegram interactor

async def telegram_set_commands(user_id: int):
    scope = BotCommandScopePeer(get_input_peer(await common.client.get_entity(user_id)))
    await common.client(SetBotCommandsRequest(scope, '', _commands[user_id]))


# Initialization

@database.connection(manual=True)
async def init(c: Connection):
    c.open()
    c.begin_transaction()
    database.commands.recalculate_commands(c=c)
    for __user in database.common.get_all_users(c):
        _categories.add(__user.id, __user.commands)
        _commands[__user.id] = bot_commands.get(__user.language, __user.commands)
        for category in __user.commands:
            _access_lists.add(category, {__user.id})
        await telegram_set_commands(__user.id)
    c.end_transaction()
    c.close()
