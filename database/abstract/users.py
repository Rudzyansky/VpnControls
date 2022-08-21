from abc import ABC, abstractmethod

from entities.user import User
from .transaction import Transaction


class Users(ABC):
    @classmethod
    @abstractmethod
    def slaves(cls, id: int, t: Transaction = None) -> list[int]: pass

    @classmethod
    @abstractmethod
    def fetch_all(cls, t: Transaction = None) -> list[User]: pass

    @classmethod
    @abstractmethod
    def fetch(cls, id: int, t: Transaction = None) -> User: pass

    @classmethod
    @abstractmethod
    def add(cls, id: int, language: str, t: Transaction = None) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_user(cls, id: int, t: Transaction = None) -> bool: pass

    @classmethod
    @abstractmethod
    def change_owner(cls, id: int, owner_id: int, t: Transaction = None) -> bool: pass

    @classmethod
    @abstractmethod
    def admin(cls, id: int, is_admin: bool, t: Transaction = None) -> bool: pass
