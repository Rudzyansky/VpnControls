import domain
from bot_commands.categories import Categories


class CategoriesUpdater:
    def __init__(self, user_id: int, append: set[Categories] = None, remove: set[Categories] = None) -> None:
        self.user_id = user_id
        self.append: set[Categories] = set() if append is None else append
        self.remove: set[Categories] = set() if remove is None else remove

    async def finish(self):
        await domain.commands.update(self.user_id, self.append, self.remove)

    def _fill(self, category: Categories, predicate: bool):
        if predicate:
            self.append.add(category)
            self.remove.discard(category)
        else:
            self.append.discard(category)
            self.remove.add(category)

    def registered(self, registered=True):
        self._fill(Categories.REGISTERED, registered)
        return self

    def can_create_account(self, count_of_accounts, accounts_limit):
        self._fill(Categories.CAN_CREATE_ACCOUNT, 0 <= count_of_accounts < accounts_limit)
        return self

    def has_accounts(self, count_of_accounts):
        self._fill(Categories.HAS_ACCOUNTS, count_of_accounts > 0)
        return self

    def can_issue_token(self, count_of_tokens, tokens_limit):
        self._fill(Categories.CAN_ISSUE_TOKEN, 0 <= count_of_tokens < tokens_limit)
        return self

    def has_tokens(self, count_of_tokens):
        self._fill(Categories.HAS_TOKENS, count_of_tokens > 0)
        return self

    def has_actual_tokens(self, count_of_actual_tokens):
        self._fill(Categories.HAS_ACTUAL_TOKENS, count_of_actual_tokens > 0)
        return self
