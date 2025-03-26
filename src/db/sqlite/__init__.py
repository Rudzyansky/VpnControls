from .accounting import AccountingRepositorySQLite
from .base import SQLiteContext
from .commands import CommandsRepositorySQLite
from .common import CommonRepositorySQLite
from .registration import RegistrationRepositorySQLite
from .schema import SCHEMA


class SQLiteRepository:
    Accounting = AccountingRepositorySQLite()
    Commands = CommandsRepositorySQLite()
    Common = CommonRepositorySQLite()
    Registration = RegistrationRepositorySQLite()

    @staticmethod
    def create_tables():
        with SQLiteContext(autocommit=True) as ctx:
            ctx.executescript(SCHEMA)


__all__ = [
    'SQLiteRepository'
]
