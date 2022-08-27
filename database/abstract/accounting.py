from abc import ABC, abstractmethod
from typing import Optional

from .connection import Connection


class Accounting(ABC):
    @classmethod
    @abstractmethod
    def get_account_position(cls, user_id: int, id: int, c: Connection = None) -> Optional[id]: pass

    @classmethod
    @abstractmethod
    def add_account(cls, user_id: int, position: int, c: Connection = None) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def move_accounts(cls, user_id: int, pos: int, diff: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_account(cls, user_id: int, pos: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_all(cls, user_id: int, c: Connection = None) -> bool: pass
