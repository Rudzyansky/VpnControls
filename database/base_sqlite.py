from abc import abstractmethod
from sqlite3 import connect


class BaseSqlite:
    database: str

    @classmethod
    def __init__(cls):
        cls.database = 'clients.db'
        cls.create_table()

    @classmethod
    def transaction(cls, func):
        connection = connect(cls.database)
        result = func(connection.cursor())
        connection.commit()
        connection.close()
        return result

    @classmethod
    @abstractmethod
    def create_table(cls): pass
