from abc import abstractmethod, ABC
from functools import wraps
from typing import Type


class Connection(ABC, object):
    @abstractmethod
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def open(self): pass

    @abstractmethod
    def close(self): pass

    @abstractmethod
    def begin_transaction(self): pass

    @abstractmethod
    def end_transaction(self): pass

    @abstractmethod
    def rollback_transaction(self): pass

    @property
    @abstractmethod
    def data(self): pass


def connection_factory(_type: Type[Connection], *_args, **_kwargs):
    def factory(auto_transaction=True, manual=False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                in_args = next(filter(lambda i: isinstance(i, Connection), args), None) is not None
                in_kwargs = isinstance(getattr(kwargs, 'c', None), Connection)
                if in_args or in_kwargs:
                    return func(*args, **kwargs)
                c = _type(*_args, **_kwargs)
                if manual:
                    return func(*args, **kwargs, c=c)
                c.open()
                if auto_transaction:
                    c.begin_transaction()
                    result = func(*args, **kwargs, c=c)
                    c.end_transaction()
                else:
                    result = func(*args, **kwargs, c=c)
                c.close()
                return result

            return wrapper

        return decorator

    return factory
