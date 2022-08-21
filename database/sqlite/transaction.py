from sqlite3 import connect, Connection, Cursor

from database.abstract.transaction import Transaction, transaction_factory


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

    def execute(self, sql, *params):
        return self.cursor.execute(sql, *params)

    def update_many(self, sql, *params):
        return self.cursor.execute(sql, *params).rowcount > 0

    def update_one(self, sql, *params):
        return self.cursor.execute(sql, *params).rowcount == 1

    def fetch_all(self, sql, *params):
        return self.cursor.execute(sql, *params).fetchall()

    def fetch_one(self, sql, *params):
        return self.cursor.execute(sql, *params).fetchone()

    def single(self, sql, *params):
        return self.cursor.execute(sql, *params).fetchone()[0]


transaction = transaction_factory(TransactionSqlite, 'clients.db')
