#
# copy from http://hopehook.com/2017/06/13/python_mysql_pool/ and do some modify
#

import logging
import threading

import pymysql
from pymysql import InterfaceError

from .errors import PoolError
from .pooling import CNX_POOL_MAXSIZE
from .pooling import PyMySQLConnectionPool, PooledPyMySQLConnection

CONNECTION_POOL_LOCK = threading.RLock()


class Connections(PyMySQLConnectionPool):

    def __init__(self, pool_size=1, pool_name=None, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
                 autocommit=True, **kwargs) -> None:

        super().__init__(pool_size=pool_size, pool_name=pool_name, charset=charset, cursorclass=cursorclass,
                         autocommit=autocommit, **kwargs)

    def connect(self):
        try:
            return self.get_connection()
        except PoolError:
            # Pool size should be lower or equal to CNX_POOL_MAXSIZE
            if self.pool_size < CNX_POOL_MAXSIZE:
                with threading.Lock():
                    new_pool_size = self.pool_size + 1
                    try:
                        self._set_pool_size(new_pool_size)
                        self._cnx_queue.maxsize = new_pool_size
                        self.add_connection()
                    except Exception as e:
                        logging.exception(e)
                    return self.connect()
            else:
                with CONNECTION_POOL_LOCK:
                    cnx = self._cnx_queue.get(block=True)
                    if not cnx.is_connected() or self._config_version != cnx._pool_config_version:
                        cnx.config(**self._cnx_config)
                        try:
                            cnx.reconnect()
                        except InterfaceError:
                            # Failed to reconnect, give connection back to pool
                            self._queue_connection(cnx)
                            raise
                        cnx._pool_config_version = self._config_version
                    return PooledPyMySQLConnection(self, cnx)
        except Exception:
            raise

    def cursor(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        return cursor

    def fetchone(self, operation, params=None):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.execute(operation, params)
            data_set = cursor.fetchone()
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        return data_set

    def fetchall(self, operation, params=None):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.execute(operation, params)
            data_set = cursor.fetchall()
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        return data_set

    def insert(self, operation, params=None, cursor_cls=None):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor(cursor=cursor_cls)
            cursor.execute(operation, params)
            last_id = cursor.lastrowid
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        return last_id

    def update(self, operation, params=None):
        return self.execute(operation, params=params)

    def delete(self, operation, params=None):
        return self.execute(operation, params=params)

    def execute(self, operation, params=None):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.execute(operation, params)
            row_count = cursor.rowcount
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        return row_count

    def executemany(self, operation, params):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor()
            cursor.executemany(operation, params)
            row_count = cursor.rowcount
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        return row_count

    def begin_transaction(self):
        cnx = self.connect()
        cnx.begin()
        return Transaction(cnx)


class Transaction(object):
    def __init__(self, connection):
        self.cnx = None
        if isinstance(connection, PooledPyMySQLConnection):
            self.cnx = connection
            self.cursor = connection.cursor()
        else:
            raise AttributeError("connection should be a PooledMySQLConnection")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            self.commit()
        else:
            # will raise with-body's Exception, should deal with it
            self.rollback()
        self.close()

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def fetchone(self, operation, params=None):
        cursor = self.cursor
        cursor.execute(operation, params)
        data_set = cursor.fetchone()
        return data_set

    def fetchall(self, operation, params=None):
        cursor = self.cursor
        cursor.execute(operation, params)
        data_set = cursor.fetchall()
        return data_set

    def insert(self, operation, params=None):
        cursor = self.cursor
        cursor.execute(operation, params)
        last_id = cursor.lastrowid
        return last_id

    def update(self, operation, params=None):
        return self.execute(operation, params=params)

    def delete(self, operation, params=None):
        return self.execute(operation, params=params)

    def execute(self, operation, params=None):
        cursor = self.cursor
        cursor.execute(operation, params)
        row_count = cursor.rowcount
        return row_count

    def executemany(self, operation, params):
        cursor = self.cursor
        cursor.executemany(operation, params)
        row_count = cursor.rowcount
        return row_count
