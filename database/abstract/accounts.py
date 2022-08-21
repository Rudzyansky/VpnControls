from abc import ABC, abstractmethod

from .transaction import Transaction


class Accounts(ABC):
    @classmethod
    @abstractmethod
    def remove_username(cls, id: int, username: str, t: Transaction = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_username(cls, id: int, username: str, new_username: str, t: Transaction = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_pos(cls, *set: tuple[int, int], t: Transaction = None) -> bool: pass
