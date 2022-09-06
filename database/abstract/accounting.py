from abc import ABC, abstractmethod
from typing import Optional

from entities.account import Account
from .connection import Connection


class Accounting(ABC):
    @classmethod
    @abstractmethod
    def get_users(cls, c: Connection = None) -> list[int]: ...

    @classmethod
    @abstractmethod
    def get_accounts(cls, user_id: int, c: Connection = None) -> list[Account]: ...

    @classmethod
    @abstractmethod
    def get_account_position(cls, user_id: int, id: int, c: Connection = None) -> Optional[int]: ...

    @classmethod
    @abstractmethod
    def get_account(cls, user_id: int, id: int, c: Connection = None) -> Optional[Account]: ...

    @classmethod
    @abstractmethod
    def get_account_by_offset(cls, user_id: int, offset: int, c: Connection = None) -> Optional[Account]: ...

    @classmethod
    @abstractmethod
    def is_username_exist(cls, username: str, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def add_account(cls, user_id: int, position: int, username: str, password: str, c: Connection = None) -> int: ...

    @classmethod
    @abstractmethod
    def set_username(cls, user_id: int, id: int, username: str, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def set_password(cls, user_id: int, id: int, password: str, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def set_position(cls, id: int, position: int, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def move_accounts(cls, user_id: int, pos: int, diff: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def remove_account(cls, user_id: int, pos: int, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def remove_all(cls, user_id: int, c: Connection = None) -> bool: ...

    @classmethod
    @abstractmethod
    def count_of_accounts(cls, user_id: int, c: Connection = None) -> int: ...
