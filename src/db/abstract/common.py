from abc import ABC, abstractmethod
from typing import Optional, List

from entities.user import User


class CommonRepositoryAbstract(ABC):
    @abstractmethod
    def get_all_users(self) -> List[User]: ...

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def set_language(self, user_id: int, lang_code: str) -> bool: ...

    #
    # unused code
    #

    @abstractmethod
    def remove_expired_tokens(self) -> bool: ...
