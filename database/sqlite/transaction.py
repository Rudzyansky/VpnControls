from sqlite3 import connect, Connection, Cursor

from database.abstract.transaction import Transaction


class TransactionSqlite(Transaction):
    database: str
    cursor: Cursor = None
    connection: Connection = None

    def __init__(self, database: str):
        self.database = database

    def begin(self):
        self.connection = connect(self.database)
        self.cursor = self.connection.cursor()
        return self.cursor

    def end(self):
        self.connection.commit()
        self.connection.close()

    @property
    def data(self):
        return self.cursor
