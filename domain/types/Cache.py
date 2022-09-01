from abc import ABC, abstractmethod
from typing import Generic, MutableMapping, TypeVar

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class Cache(ABC, Generic[_KT, _VT]):
    _data: MutableMapping[_KT, _VT]

    def __init__(self) -> None:
        self._data = dict[_KT: _VT]()

    @abstractmethod
    def __setitem__(self, _k: _KT, _v: _VT): ...

    @abstractmethod
    def __getitem__(self, _k: _KT) -> _VT: ...

    @abstractmethod
    def add(self, _k: _KT, _v: _VT): ...

    @abstractmethod
    def remove(self, _k: _KT, _v: _VT): ...
