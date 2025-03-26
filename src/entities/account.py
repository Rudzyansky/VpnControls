from dataclasses import dataclass


@dataclass
class Account:
    id: int = None
    username: str = None
    password: str = None
