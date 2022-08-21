from abc import ABC, abstractmethod

from entities.user import User
from .connection import Connection


class Users(ABC):
    @classmethod
    @abstractmethod
    def slaves(cls, id: int, c: Connection = None) -> list[int]: pass

    @classmethod
    @abstractmethod
    def fetch_all(cls, c: Connection = None) -> list[User]: pass

    @classmethod
    @abstractmethod
    def fetch(cls, id: int, c: Connection = None) -> User: pass

    @classmethod
    @abstractmethod
    def add(cls, id: int, language: str, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_user(cls, id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_owner(cls, id: int, owner_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def admin(cls, id: int, is_admin: bool, c: Connection = None) -> bool: pass
