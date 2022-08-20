from abc import ABC, abstractmethod
# noinspection PyShadowingBuiltins
from typing import Optional

from entities.token import Token


class Tokens(ABC):
    @classmethod
    @abstractmethod
    def remove_expired(cls) -> bool: pass

    @classmethod
    @abstractmethod
    def get_all(cls, owner_id: int) -> list: pass

    @classmethod
    @abstractmethod
    def is_accept_invite(cls, user_id: int) -> bool: pass

    @classmethod
    @abstractmethod
    def get_owner(cls, user_id: int) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def use(cls, token: Token) -> bool: pass

    @classmethod
    @abstractmethod
    def revoke(cls, token: Token) -> bool: pass

    @classmethod
    @abstractmethod
    def add(cls, token: Token) -> bool: pass

    @classmethod
    @abstractmethod
    def fetch(cls, token: Token) -> Optional[Token]: pass
