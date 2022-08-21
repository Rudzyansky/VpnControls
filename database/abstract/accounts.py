from abc import ABC, abstractmethod

from .connection import Connection


class Accounts(ABC):
    @classmethod
    @abstractmethod
    def remove_username(cls, id: int, username: str, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_username(cls, id: int, username: str, new_username: str, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_pos(cls, *set: tuple[int, int], c: Connection = None) -> bool: pass
