from abc import ABC, abstractmethod


class Controls(ABC):
    @classmethod
    @abstractmethod
    def add_user(cls, username: str): pass

    @classmethod
    @abstractmethod
    def remove_user(cls, username: str): pass

    @classmethod
    @abstractmethod
    def reset_password(cls, username: str): pass

    @classmethod
    @abstractmethod
    def change_username(cls, username: str, new_username: str): pass
