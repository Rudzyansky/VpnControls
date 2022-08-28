from abc import ABC, abstractmethod
from typing import Optional

from entities.account import Account


class Controls(ABC):
    @classmethod
    @abstractmethod
    def add_user(cls, user_id: int, username: str, password: str) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def remove_user(cls, user_id: int, id: int) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def set_password(cls, user_id: int, id: int, password: str) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def set_username(cls, user_id: int, id: int, username: str) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def get_account(cls, user_id: int, id: int) -> Optional[tuple[str, str]]: pass

    @classmethod
    @abstractmethod
    def get_accounts(cls, user_id: int, *ids: int) -> list[tuple[str, str]]: pass

    @classmethod
    @abstractmethod
    def change_hook(cls): pass
