from abc import ABC, abstractmethod
from typing import Optional

from entities.token import Token
from .connection import Connection


class Registration(ABC):
    @classmethod
    @abstractmethod
    def is_accept_invite(cls, user_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def add_user(cls, user_id: int, language: str, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def revoke_token(cls, token: bytes, owner_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def revoke_token_by_user_id(cls, user_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def free_token_by_user_id(cls, user_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def use_token(cls, token: bytes, owner_id: int, user_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def add_token(cls, token: bytes, owner_id: int, c: Connection = None) -> bool: pass

    @classmethod
    @abstractmethod
    def get_token(cls, token: bytes, owner_id: int, c: Connection = None) -> Optional[Token]: pass

    @classmethod
    @abstractmethod
    def get_all_tokens(cls, owner_id: int, c: Connection = None) -> list[Token]: pass

    @classmethod
    @abstractmethod
    def get_actual_tokens(cls, owner_id: int, c: Connection = None) -> list[Token]: pass
