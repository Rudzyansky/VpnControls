from abc import ABC, abstractmethod
from typing import Optional, List

from entities.account import Account


class AccountingRepositoryAbstract(ABC):
    @abstractmethod
    def get_users(self) -> List[int]: ...

    @abstractmethod
    def get_accounts(self, user_id: int) -> List[Account]: ...

    @abstractmethod
    def get_account_position(self, user_id: int, account_id: int) -> Optional[int]: ...

    @abstractmethod
    def get_account(self, user_id: int, account_id: int) -> Optional[Account]: ...

    @abstractmethod
    def get_account_by_offset(self, user_id: int, offset: int) -> Optional[Account]: ...

    @abstractmethod
    def is_username_exist(self, username: str) -> bool: ...

    @abstractmethod
    def add_account(self, user_id: int, position: int, username: str, password: str) -> int: ...

    @abstractmethod
    def set_username(self, user_id: int, account_id: int, username: str) -> bool: ...

    @abstractmethod
    def set_password(self, user_id: int, account_id: int, password: str) -> bool: ...

    @abstractmethod
    def set_position(self, account_id: int, position: int) -> bool: ...

    @abstractmethod
    def move_accounts(self, user_id: int, position: int, diff: int) -> bool: ...

    @abstractmethod
    def remove_account(self, user_id: int, account_id: int) -> bool: ...

    @abstractmethod
    def remove_all(self, user_id: int) -> bool: ...

    @abstractmethod
    def count_of_accounts(self, user_id: int) -> int: ...
