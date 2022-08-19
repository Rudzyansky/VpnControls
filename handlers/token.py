from uuid import UUID, uuid4


class Token:
    data: UUID
    expire: str
    used_by: int
    owner_id: int

    def __init__(self, data=None, expire: str = None, used_by: int = None, owner_id: int = None) -> None:
        if data is None:
            self.data = uuid4()
        elif isinstance(data, str):
            self.data = UUID(data.lower())
        elif isinstance(data, bytes):
            self.data = UUID(bytes=data)
        else:
            raise RuntimeError(f'Token: Not allowed type "{type(data)}"')
        self.expire = expire
        self.used_by = used_by
        self.owner_id = owner_id

    def __str__(self) -> str:
        return self.str

    @property
    def str(self) -> str:
        return str(self.data).upper()

    @property
    def bytes(self) -> bytes:
        return self.data.bytes
