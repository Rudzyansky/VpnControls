from abc import ABC, abstractmethod

from .connection import Connection


class Privileges(ABC):
    @classmethod
    @abstractmethod
    def get_users_page(cls, owner_id: int, offset: int, count: int, c: Connection = None) -> list[int]: pass

    @classmethod
    @abstractmethod
    def get_users_count(cls, owner_id: int, c: Connection = None) -> int: pass
