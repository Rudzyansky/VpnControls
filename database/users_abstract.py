from abc import ABC, abstractmethod

# noinspection PyShadowingBuiltins
from entities.user import User


class Users(ABC):
    @classmethod
    @abstractmethod
    def slaves(cls, id: int) -> list[int]: pass

    @classmethod
    @abstractmethod
    def fetch_all(cls) -> list[User]: pass

    @classmethod
    @abstractmethod
    def fetch(cls, id: int) -> User: pass

    @classmethod
    @abstractmethod
    def is_registered(cls, id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def is_admin(cls, id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def add(cls, id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_user(cls, id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def change_owner(cls, id: int, owner_id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def admin(cls, id: int, is_admin: bool) -> bool: pass
