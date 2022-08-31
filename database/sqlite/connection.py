import sqlite3

import env
from database.abstract.connection import Connection, connection_factory


class ConnectionSqlite(Connection):
    database: str
    cursor: sqlite3.Cursor = None
    connection: sqlite3.Connection = None

    def __init__(self, database: str):
        self.database = database

    def open(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def begin_transaction(self):
        # self.connection.execute('BEGIN TRANSACTION')
        pass

    def end_transaction(self):
        # self.connection.execute('END TRANSACTION')
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    @property
    def data(self):
        return self.cursor

    def execute(self, sql, *params):
        return self.cursor.execute(sql, params)

    def update_many(self, sql, *params):
        return self.cursor.execute(sql, params).rowcount > 0

    def update_one(self, sql, *params):
        return self.cursor.execute(sql, params).rowcount == 1

    def fetch_all(self, sql, *params):
        return self.cursor.execute(sql, params).fetchall()

    def fetch_one(self, sql, *params):
        return self.cursor.execute(sql, params).fetchone()

    def single(self, sql, *params):
        return self.cursor.execute(sql, params).fetchone()[0]


connection = connection_factory(ConnectionSqlite, env.DB_PATH)
