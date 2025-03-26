from typing import Generic, TypeVar

from domain.types.cache import Cache

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class CacheList(Cache[_KT, list[_VT]], Generic[_KT, _VT]):
    def __setitem__(self, key: _KT, values: list[_VT]):
        data = self._data.get(key)
        if data is None:
            data = list[_VT]()
            self._data[key] = data
        else:
            data.clear()
        data.extend(values)

    def __getitem__(self, key: _KT) -> list[_VT]:
        data = self._data.get(key)
        if data is None:
            data = list[_VT]()
            self._data[key] = data
        return data

    def add(self, key: _KT, values: list[_VT]):
        if key in self._data.keys():
            self._data[key].extend(values)
        else:
            self._data[key] = values.copy()

    def remove(self, key: _KT, values: list[_VT]):
        if key in self._data.keys():
            data = self._data[key]
            for value in values:
                if value in data:
                    data.remove(value)
