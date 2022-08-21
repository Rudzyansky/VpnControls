from abc import ABC, abstractmethod

from database.abstract import Transaction


class Accounts(ABC):
    @classmethod
    @abstractmethod
    def remove_username(cls, id: int, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def change_username(cls, id: int, new_username: str, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def change_pos(cls, *set: tuple[int, int], t: Transaction) -> bool: pass
