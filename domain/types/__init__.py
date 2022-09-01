from telethon.tl.types import BotCommand

from bot_commands.categories import Categories
from domain.types.cache_list import CacheList
from domain.types.cache_set import CacheSet
from domain.types.categories_updater import CategoriesUpdater

CategoriesCache = CacheSet[int, Categories]
CommandsCache = CacheList[int, BotCommand]
AccessListsCache = CacheSet[Categories, int]

__all__ = [
    'CategoriesCache',
    'CommandsCache',
    'AccessListsCache',
    'CategoriesUpdater',
]
