from abc import ABC, abstractmethod

from entities.user import User


class CommandsRepositoryAbstract(ABC):
    @abstractmethod
    def recalculate_commands(self, user_id: int = None) -> list[User]: ...

    @abstractmethod
    def set_user_commands(self, user_id: int, commands: int) -> bool: ...
