from dataclasses import dataclass
from typing import Optional

from entities.account import Account


@dataclass
class GetAccount:
    offset: int = 0
    count: int = 0
    data: Optional[Account] = None


@dataclass
class ChangeUsername:
    username_exist: bool = False
    changed: bool = False
    data: Optional[Account] = None


@dataclass
class ChangePassword:
    changed: bool = False
    data: Optional[Account] = None
