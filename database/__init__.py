from .abstract import Common, Registration
from .sqlite import CommonSqlite, RegistrationSqlite, connection, init

init()

common: Common = CommonSqlite()
registration: Registration = RegistrationSqlite()

__all__ = [
    'common', 'registration', 'connection'
]
