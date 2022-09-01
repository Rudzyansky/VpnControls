from telethon.tl.types import BotCommand

from bot_commands.categories import Categories
from domain.types.CacheList import CacheList
from domain.types.CacheSet import CacheSet

CategoriesCache = CacheSet[int, Categories]
CommandsCache = CacheList[int, BotCommand]
AccessListsCache = CacheSet[Categories, int]

__all__ = [
    'CategoriesCache',
    'CommandsCache',
    'AccessListsCache',
]
