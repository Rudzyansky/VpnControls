from telethon import TelegramClient
from telethon.tl.functions.bots import SetBotCommandsRequest, ResetBotCommandsRequest
from telethon.tl.types import BotCommand, BotCommandScopePeer
from telethon.utils import get_input_peer

import bot_commands
import database
from bot_commands.categories import Categories
from entities.user import User


class Commands:
    _cache: dict[int:list[BotCommand]] = dict()
    _cache_categories: dict[int:set[Categories]] = dict()

    def __init__(self, common_db: database.Common) -> None:
        super().__init__()
        self.common_db = common_db
        for user in common_db.get_all_users():
            self._cache_categories[user.id] = user.commands
            self._recalculate_cache(user)

    # noinspection PyMethodMayBeStatic
    async def _telegram_reset_commands(self, client: TelegramClient, user: User):
        scope = BotCommandScopePeer(get_input_peer(await client.get_entity(user.id)))
        await client(ResetBotCommandsRequest(scope, user.language))

    async def _telegram_set_commands(self, client: TelegramClient, user: User):
        scope = BotCommandScopePeer(get_input_peer(await client.get_entity(user.id)))
        await client(SetBotCommandsRequest(scope, user.language, self._cache[user.id]))

    def _recalculate_cache(self, user: User):
        self._cache[user.id] = bot_commands.get(user.language, self._cache_categories[user.id])

    def _set_user_commands_db(self, user: User):
        self.common_db.set_user_commands(user.id, user.commands_int)

    async def refresh_commands(self, client: TelegramClient, user: User):
        await self._telegram_set_commands(client, user)

    async def set_commands(self, client: TelegramClient, user: User, *categories: Categories):
        self._cache_categories[user.id] = set(categories)
        self._recalculate_cache(user)
        self._set_user_commands_db(user)
        await self._telegram_set_commands(client, user)

    async def add_commands(self, client: TelegramClient, user: User, *categories: Categories):
        self._cache_categories[user.id] += set(categories)
        self._recalculate_cache(user)
        self._set_user_commands_db(user)
        await self._telegram_set_commands(client, user)

    async def delete_commands(self, client: TelegramClient, user: User, *categories: Categories):
        self._cache_categories[user.id] -= set(categories)
        self._recalculate_cache(user)
        self._set_user_commands_db(user)
        await self._telegram_set_commands(client, user)


commands = Commands(
    database.common
)
