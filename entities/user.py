from dataclasses import dataclass, field, InitVar
from functools import reduce

from bot_commands.categories import Categories, decompose_categories


@dataclass
class User:
    id: int
    tokens_limit: int = 0
    accounts_limit: int = 1
    language: str = 'en'
    commands: set[Categories] = field(init=False)
    _commands: InitVar[int] = None

    @property
    def commands_int(self):
        return reduce(lambda a, b: a | b, self.commands).conjugate()

    def __post_init__(self, _commands) -> None:
        super().__init__()
        if _commands is None:
            self.commands = set()
        else:
            self.commands = decompose_categories(Categories(_commands))
