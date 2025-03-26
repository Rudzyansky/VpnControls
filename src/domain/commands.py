from functools import reduce

from telegram import BotCommandScopeChat
from telegram.ext import ExtBot

import bot_commands
import domain.common
from bot_commands.categories import Categories
from db import Repository
from domain.types import *

# Declarations

_categories: CategoriesCache = CategoriesCache()
_commands: CommandsCache = CommandsCache()
_access_lists: AccessListsCache = AccessListsCache()


# Access lists cache

def access_list(category: Categories):
    return _access_lists[category]


# Commands cache

async def update(user_id: int, append: set[Categories] = None, remove: set[Categories] = None):
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
    Repository.Commands.set_user_commands(user_id, current_int)

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
    # noinspection PyUnresolvedReferences
    bot: ExtBot = domain.common.application.bot
    await bot.set_my_commands(
        commands=_commands[user_id],
        scope=BotCommandScopeChat(user_id)
    )


# Initialization

def init():
    Repository.Commands.recalculate_commands()
    for __user in Repository.Common.get_all_users():
        _categories.add(__user.id, __user.commands)
        _commands[__user.id] = bot_commands.get(__user.language, __user.commands)
        for category in __user.commands:
            _access_lists.add(category, {__user.id})
        # await telegram_set_commands(__user.id)
