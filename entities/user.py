from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_admin: bool = False
    accounts_limit: int = 1
    language: str = 'en'
