from dataclasses import dataclass, field


@dataclass
class UsersMeta:
    @dataclass
    class User:
        id: int
        display_name: str

    page: int = 1
    pages_count: int = 0
    users: list[User] = field(default_factory=list)
