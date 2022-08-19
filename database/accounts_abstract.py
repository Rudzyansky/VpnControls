from abc import ABC, abstractmethod


# noinspection PyShadowingBuiltins
class Accounts(ABC):
    @classmethod
    @abstractmethod
    def remove_username(cls, id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def change_username(cls, id: int, new_username: str) -> bool: pass

    @classmethod
    @abstractmethod
    def change_pos(cls, *set: tuple[int, int]) -> bool: pass
