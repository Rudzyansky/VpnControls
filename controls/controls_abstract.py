from abc import ABC
from functools import wraps
from typing import Optional


def update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args[0].update_hook()
        return result

    return wrapper


class Controls(ABC):
    def add_user(self, user_id: int, username: str, password: str) -> int: ...

    def remove_user(self, user_id: int, id: int) -> Optional[int]: ...

    def set_password(self, user_id: int, id: int, password: str) -> Optional[int]: ...

    def set_username(self, user_id: int, id: int, username: str) -> Optional[int]: ...

    def get_account(self, user_id: int, id: int) -> Optional[tuple[str, str]]: ...

    def get_accounts(self, user_id: int, *ids: int) -> list[tuple[str, str]]: ...

    def update_hook(self): ...
