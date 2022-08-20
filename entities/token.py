from dataclasses import dataclass, field, InitVar
from typing import Union
from uuid import UUID, uuid4


@dataclass
class Token:
    _data: UUID = field(init=False)
    data: InitVar[Union[None, str, bytes]] = None
    expire: str = None
    used_by: int = None
    owner_id: int = None
    language: str = None

    def __post_init__(self, data) -> None:
        if data is None:
            self._data = uuid4()
        elif isinstance(data, str):
            self._data = UUID(data.lower())
        elif isinstance(data, bytes):
            self._data = UUID(bytes=data)
        else:
            raise RuntimeError(f'Token: Not allowed type "{type(data)}"')

    def __str__(self):
        return str(self._data).upper()

    @property
    def bytes(self):
        return self._data.bytes
