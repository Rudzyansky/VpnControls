from functools import wraps
from typing import Type

from .accounts import Accounts
from .tokens import Tokens
from .transaction import Transaction
from .users import Users


def transaction_factory(_type: Type[Transaction], *_args, **_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            in_args = next(filter(lambda i: isinstance(i, Transaction), args), None) is not None
            in_kwargs = hasattr(kwargs, 't')
            if in_args or in_kwargs:
                return func(*args, **kwargs)
            t = _type(*_args, **_kwargs)
            t.begin()
            result = func(*args, **kwargs, t=t)
            t.end()
            return result

        return wrapper

    return decorator


__all__ = [
    'Accounts',
    'Tokens',
    'Users',
    'Transaction',
    'transaction_factory'
]
