from abc import ABC, abstractmethod

from entities.user import User
from .connection import Connection


class Commands(ABC):
    @classmethod
    @abstractmethod
    def recalculate_commands(cls, user_id: int = None, c: Connection = None) -> list[User]: pass

    @classmethod
    @abstractmethod
    def set_user_commands(cls, user_id: int, commands: int, c: Connection = None) -> bool: pass
