from abc import ABC, abstractmethod
from typing import Optional

from entities.user import User
from .connection import Connection


class Common(ABC):
    @classmethod
    @abstractmethod
    def get_all_users(cls, c: Connection = None) -> list[User]: pass

    @classmethod
    @abstractmethod
    def get_user(cls, user_id: int, c: Connection = None) -> Optional[User]: pass

    @classmethod
    @abstractmethod
    def set_user_commands(cls, user_id: int, commands: int, c: Connection = None) -> bool: pass

    #
    # unused code
    #

    @classmethod
    @abstractmethod
    def remove_expired_tokens(cls, c: Connection = None) -> bool: pass
