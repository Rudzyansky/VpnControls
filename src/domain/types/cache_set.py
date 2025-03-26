from typing import Generic, TypeVar

from domain.types.cache import Cache

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class CacheSet(Cache[_KT, set[_VT]], Generic[_KT, _VT]):
    def __setitem__(self, key: _KT, values: list[_VT]):
        data = self._data.get(key)
        if data is None:
            data = set[_VT]()
            self._data[key] = data
        else:
            data.clear()
        data.update(values)

    def __getitem__(self, key: _KT) -> set[_VT]:
        data = self._data.get(key)
        if data is None:
            data = set[_KT]()
            self._data[key] = data
        return data

    def add(self, key: _KT, values: set[_VT]):
        if len(values) > 0:
            if key in self._data.keys():
                self._data[key].update(values)
            else:
                self._data[key] = values.copy()

    def remove(self, key: _KT, values: set[_VT]):
        if len(values) > 0:
            if key in self._data.keys():
                self._data[key].difference_update(values)
