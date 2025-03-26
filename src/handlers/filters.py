from typing import Optional, Union

from telegram import Update
from telegram.ext import filters
# noinspection PyProtectedMember
from telegram.ext._utils.types import FilterDataDict

from bot_commands.categories import Categories
from domain.commands import access_list
from domain.registration import is_accept_invite


class CategoryFilter(filters.UpdateFilter):
    def __init__(self, category: Categories):
        super().__init__(name=f"Category({category.name})", data_filter=False)
        self.category = category

    def filter(self, update: Update) -> Optional[Union[bool, FilterDataDict]]:
        return update.effective_user.id in access_list(self.category)


class CanRegisterFilter(filters.UpdateFilter):
    def __init__(self):
        super().__init__(name="CanRegister()", data_filter=False)

    def filter(self, update: Update) -> Optional[Union[bool, FilterDataDict]]:
        return is_accept_invite(update.effective_chat.id)


class UsernameChangeFilter(filters.UpdateFilter):
    def __init__(self):
        super().__init__(name="UsernameChange()", data_filter=False)
        self._access_list = set()

    def filter(self, update: Update) -> Optional[Union[bool, FilterDataDict]]:
        return update.effective_user.id in self._access_list

    def add_user(self, user_id: int):
        self._access_list.add(user_id)

    def remove_user(self, user_id: int):
        self._access_list.discard(user_id)


# Predefined filters for each category
registered = CategoryFilter(Categories.REGISTERED)
can_invite = CategoryFilter(Categories.HAS_ACTUAL_TOKENS)
has_accounts = CategoryFilter(Categories.HAS_ACCOUNTS)
can_create_account = CategoryFilter(Categories.CAN_CREATE_ACCOUNT)
can_issue_token = CategoryFilter(Categories.CAN_ISSUE_TOKEN)
has_actual_tokens = CategoryFilter(Categories.HAS_ACTUAL_TOKENS)
has_tokens = CategoryFilter(Categories.HAS_TOKENS)
has_users = CategoryFilter(Categories.HAS_USERS)

# State management filters
username_change = UsernameChangeFilter()

can_register = CanRegisterFilter()
