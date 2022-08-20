from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    is_admin: bool = None
    accounts_limit: int = None
    language: str = None
