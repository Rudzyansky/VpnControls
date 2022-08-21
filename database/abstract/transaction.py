from abc import abstractmethod, ABC
from functools import wraps
from typing import Type


class Transaction(ABC, object):
    @abstractmethod
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def begin(self): pass

    @abstractmethod
    def end(self): pass

    @property
    @abstractmethod
    def data(self): pass


def transaction_factory(_type: Type[Transaction], *_args, **_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            in_args = next(filter(lambda i: isinstance(i, Transaction), args), None) is not None
            in_kwargs = isinstance(getattr(kwargs, 't', None), Transaction)
            if in_args or in_kwargs:
                return func(*args, **kwargs)
            t = _type(*_args, **_kwargs)
            t.begin()
            result = func(*args, **kwargs, t=t)
            t.end()
            return result

        return wrapper

    return decorator
