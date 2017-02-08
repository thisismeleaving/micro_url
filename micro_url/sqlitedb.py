import sqlite3
from contextlib import contextmanager


class sqliteDB():
    """A convenience utility to manage database connections"""

    def __init__(self):
        self.__conn = None
        self.__cursor = None

        self.__conn = sqlite3.connect('micro_url.db', isolation_level=None)
        self.__conn.row_factory = dict_factory

    def get_cursor(self):
        return self.__conn.cursor()

    def close(self):
        if self.__cursor:
            self.__cursor.close()

        if self.__conn:
            self.__conn.close()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@contextmanager
def cursor():
    try:
        db = sqliteDB()
        dbc = db.get_cursor()
        yield dbc
    finally:
        db.close()
