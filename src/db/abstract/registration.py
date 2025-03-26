from abc import ABC, abstractmethod
from typing import Optional, List

from entities.token import Token
from entities.user import User


class RegistrationRepositoryAbstract(ABC):
    @abstractmethod
    def is_accept_invite(self, user_id: int) -> bool: ...

    @abstractmethod
    def add_user(self, user: User) -> bool: ...

    @abstractmethod
    def revoke_token(self, token: bytes, owner_id: int) -> bool: ...

    @abstractmethod
    def revoke_token_by_user_id(self, user_id: int) -> bool: ...

    @abstractmethod
    def free_token_by_user_id(self, user_id: int) -> bool: ...

    @abstractmethod
    def use_token(self, token: bytes, owner_id: int, user_id: int) -> bool: ...

    @abstractmethod
    def add_token(self, token: bytes, owner_id: int) -> bool: ...

    @abstractmethod
    def get_token(self, token: bytes) -> Optional[Token]: ...

    @abstractmethod
    def fetch_token(self, token: bytes, owner_id: int) -> Optional[Token]: ...

    @abstractmethod
    def get_all_tokens(self, owner_id: int) -> List[Token]: ...

    @abstractmethod
    def get_actual_tokens(self, owner_id: int) -> List[Token]: ...

    @abstractmethod
    def get_tokens_limit(self, user_id: int) -> int: ...

    @abstractmethod
    def count_of_tokens(self, owner_id: int) -> int: ...

    @abstractmethod
    def get_next_actual_token(self, owner_id: int, offset: int) -> Token: ...

    @abstractmethod
    def count_of_actual_tokens(self, owner_id: int) -> int: ...
