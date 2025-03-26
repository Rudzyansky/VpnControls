import sqlite3
import threading
from pathlib import Path
from typing import TypeVar, Mapping, TypeAlias, Iterable, Any, List, Dict, Literal, Protocol

import config

_T = TypeVar('_T')
_T_co = TypeVar("_T_co", covariant=True)


class SupportsLenAndGetItem(Protocol[_T_co]):
    def __len__(self) -> int: ...

    def __getitem__(self, k: int, /) -> _T_co: ...


_ParametersType: TypeAlias = (
        SupportsLenAndGetItem[str | int | float | None] |
        Mapping[str, str | int | float | None]
)
_OutputType: TypeAlias = Literal['auto', 'fetchall', 'fetchone', 'scalar', 'lastrowid', 'rowcount']

_lock = threading.Lock()


# def synchronize(fn: Callable[..., _T]):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs) -> _T:
#         with _lock:
#             return fn(*args, **kwargs)
#
#     return wrapper


class SQLiteContext:

    def __init__(self, autocommit: bool = False, db_path: str | Path = config.DB_PATH):
        self.__connection: sqlite3.Connection | None = None
        self.__cursor: sqlite3.Cursor | None = None
        self.__db_path = str(db_path)
        self.__autocommit = autocommit

    @property
    def connection(self) -> sqlite3.Connection:
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor

    def execute(self, sql: str, parameters: _ParametersType = ()):
        self.__cursor.execute(sql, parameters)
        return self

    def executemany(self, sql: str, seq_of_parameters: Iterable[_ParametersType]):
        self.__cursor.executemany(sql, seq_of_parameters)
        return self

    def executescript(self, sql_script: str):
        self.__cursor.executescript(sql_script)
        return self

    def fetchone(self, columns: bool = False) -> Any:
        row = self.__cursor.fetchone()
        if columns and row:
            __columns = [d[0] for d in self.__cursor.description[0]]
            return {key: value for key, value in zip(__columns, row)}
        else:
            return row

    def fetchall(self, columns: bool = False) -> List | List[Dict[str, Any]]:
        rows = self.__cursor.fetchall()
        if columns and rows:
            __columns = [d[0] for d in self.__cursor.description[0]]
            return [{key: value for key, value in zip(__columns, row)} for row in rows]
        else:
            return rows

    def fetchmany(self, size: int | None = 1, columns: bool = False) -> List:
        rows = self.__cursor.fetchmany(size)
        if columns and rows:
            __columns = [d[0] for d in self.__cursor.description[0]]
            return [{key: value for key, value in zip(__columns, row)} for row in rows]
        else:
            return rows

    def scalar(self) -> Any:
        return self.__cursor.fetchone()[0]

    def commit(self):
        self.__connection.commit()
        return self

    def __enter__(self):
        _lock.acquire()
        self.__connection = sqlite3.connect(self.__db_path)
        self.__cursor = self.__connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__autocommit:
            self.__connection.commit()
        self.__cursor.close()
        self.__connection.close()
        self.__cursor = None
        self.__connection = None
        _lock.release()


class SQLiteBase:
    cm = SQLiteContext

    def query(self, sql: str, parameters: _ParametersType = (), output: _OutputType = 'auto'):
        with self.cm(autocommit=True) as ctx:
            ctx.execute(sql, parameters)
            if output == 'auto':
                sql_lower = sql.lower()
                if sql_lower.startswith(('delete', 'update')):
                    output = 'rowcount'
                elif sql_lower.startswith('insert'):
                    output = 'lastrowid'
                elif sql_lower.startswith('select'):
                    output = 'fetchall'

            if output == 'fetchall':
                return ctx.fetchall()
            if output == 'fetchone':
                return ctx.fetchone()
            if output == 'scalar':
                return ctx.scalar()
            if output == 'rowcount':
                return ctx.cursor.rowcount
            if output == 'lastrowid':
                return ctx.cursor.lastrowid
