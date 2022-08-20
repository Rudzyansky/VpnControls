from abc import abstractmethod
from functools import wraps
from sqlite3 import connect

database: str = 'clients.db'


class BaseSqlite:

    @classmethod
    def __init__(cls):
        cls.create_table()

    @classmethod
    @abstractmethod
    def create_table(cls): pass


def transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect(database)
        result = func(*args, **kwargs, c=connection.cursor())
        connection.commit()
        connection.close()
        return result

    return wrapper
