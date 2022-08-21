from abc import ABC, abstractmethod
from typing import Optional

from entities.token import Token
from . import Transaction


class Tokens(ABC):
    @classmethod
    @abstractmethod
    def remove_expired(cls, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def get_all(cls, owner_id: int, t: Transaction) -> list: pass

    @classmethod
    @abstractmethod
    def is_accept_invite(cls, user_id: int, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def get_owner(cls, user_id: int, t: Transaction) -> Optional[int]: pass

    @classmethod
    @abstractmethod
    def use(cls, token: Token, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def revoke(cls, token: Token, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def revoke_by_used(cls, user_id: int, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def add(cls, token: Token, t: Transaction) -> bool: pass

    @classmethod
    @abstractmethod
    def fetch(cls, token: Token, t: Transaction) -> Optional[Token]: pass
