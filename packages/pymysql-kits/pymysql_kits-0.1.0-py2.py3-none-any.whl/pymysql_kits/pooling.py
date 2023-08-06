# This program is copy from mysql-connector-python pooling.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.

"""
Implementing pooling of connections to PyMySQL.
"""

import re
import threading
from uuid import uuid4

from pymysql.connections import Connection

try:
    import queue
except ImportError:
    # Python v2
    import Queue as queue

from .errors import *

CONNECTION_POOL_LOCK = threading.RLock()
CNX_POOL_MAXSIZE = 32
CNX_POOL_MAXNAMESIZE = 64
CNX_POOL_NAMEREGEX = re.compile(r'[^a-zA-Z0-9._:\-*$#]')


def generate_pool_name(**kwargs):
    """Generate a pool name

    This function takes keyword arguments, usually the connection
    arguments for Connection, and tries to generate a name for
    a pool.

    Raises PoolError when no name can be generated.

    Returns a string.
    """
    parts = []
    for key in ('host', 'port', 'user', 'database'):
        try:
            parts.append(str(kwargs[key]))
        except KeyError:
            pass

    if not parts:
        raise PoolError("Failed generating pool name; specify pool_name")

    return '_'.join(parts)


def is_connected(cnx):
    """Reports whether the connection to MySQL Server is available

    This method checks whether the connection to MySQL is available.
    It is similar to ping(), but unlike the ping()-method, either True
    or False is returned and no exception is raised.

    Returns True or False.
    """
    try:
        cnx.ping(reconnect=False)
    except:
        return False
    return True


class PooledPyMySQLConnection(object):
    """Class holding a Connection in a pool

    PooledPyMySQLConnection is used by PyMySQLConnectionPool to return an
    instance holding a MySQL connection. It works like a Connection
    except for methods like close() and config().

    The close()-method will add the connection back to the pool rather
    than disconnecting from the MySQL server.

    Configuring the connection have to be done through the PyMySQLConnectionPool
    method set_config(). Using config() on pooled connection will raise a
    PoolError.
    """

    def __init__(self, pool, cnx):
        """Initialize

        The pool argument must be an instance of PyMySQLConnectionPool. cnx
        if an instance of Connection.
        """
        if not isinstance(pool, PyMySQLConnectionPool):
            raise AttributeError("pool should be a PyMySQLConnectionPool")
        if not isinstance(cnx, Connection):
            raise AttributeError("cnx should be a Connection")
        self._cnx_pool = pool
        self._cnx = cnx

    def __getattr__(self, attr):
        """Calls attributes of the Connection instance"""
        return getattr(self._cnx, attr)

    def close(self):
        """Do not close, but add connection back to pool

        The close() method does not close the connection with the
        MySQL server. The connection is added back to the pool so it
        can be reused.

        """
        self._cnx_pool.add_connection(self._cnx)
        self._cnx = None

    def config(self, **kwargs):
        """Configuration is done through the pool"""
        raise PoolError("Configuration for pooled connections should be done through the pool itself.")

    @property
    def pool_name(self):
        """Return the name of the connection pool"""
        return self._cnx_pool.pool_name


class PyMySQLConnectionPool(object):
    """Class defining a pool of MySQL connections"""

    def __init__(self, pool_size=5, pool_name=None, **kwargs) -> None:
        """Initialize

        Initialize a MySQL connection pool with a maximum number of
        connections set to pool_size. The rest of the keywords
        arguments, kwargs, are configuration arguments for Connection
        instances.
        """
        self._pool_size = None
        self._pool_name = None

        self._set_pool_size(pool_size)
        self._set_pool_name(pool_name or generate_pool_name(**kwargs))
        self._cnx_config = {}
        self._cnx_queue = queue.Queue(self._pool_size)
        self._config_version = uuid4()

        if kwargs:
            self.set_config(**kwargs)
            cnt = 0
            while cnt < self._pool_size:
                self.add_connection()
                cnt += 1

    @property
    def pool_name(self):
        """Return the name of the connection pool"""
        return self._pool_name

    @property
    def pool_size(self):
        """Return number of connections managed by the pool"""
        return self._pool_size

    def set_config(self, **kwargs):
        """Set the connection configuration for Connection instances

        This method sets the configuration used for creating Connection
        instances. See Connection for valid connection arguments.

        Raises PoolError when a connection argument is not valid, missing
        or not supported by Connection.
        """
        if not kwargs:
            return

        with CONNECTION_POOL_LOCK:
            try:
                if "use_pure" in kwargs:
                    del kwargs["use_pure"]
                self._cnx_config = kwargs
                self._config_version = uuid4()
            except AttributeError as err:
                raise PoolError("Connection configuration not valid: {0}".format(err))

    def _set_pool_size(self, pool_size):
        """Set the size of the pool

        This method sets the size of the pool but it will not resize the pool.

        Raises an AttributeError when the pool_size is not valid. Invalid size
        is 0, negative or higher than pooling.CNX_POOL_MAXSIZE.
        """
        if pool_size <= 0 or pool_size > CNX_POOL_MAXSIZE:
            raise AttributeError("Pool size should be higher than 0 and lower or equal to {0}".format(CNX_POOL_MAXSIZE))

        self._pool_size = pool_size

    def _set_pool_name(self, pool_name):
        """Set the name of the pool

        This method checks the validity and sets the name of the pool.

        Raises an AttributeError when pool_name contains illegal characters
        ([^a-zA-Z0-9._\-*$#]) or is longer than pooling.CNX_POOL_MAXNAMESIZE.
        """
        if CNX_POOL_NAMEREGEX.search(pool_name):
            raise AttributeError("Pool name '{0}' contains illegal characters".format(pool_name))

        if len(pool_name) > CNX_POOL_MAXNAMESIZE:
            raise AttributeError("Pool name '{0}' is too long".format(pool_name))

        self._pool_name = pool_name

    def _queue_connection(self, cnx):
        """Put connection back in the queue

        This method is putting a connection back in the queue. It will not
        acquire a lock as the methods using _queue_connection() will have it
        set.

        Raises PoolError on errors.
        """
        if not isinstance(cnx, Connection):
            raise PoolError("Connection instance not subclass of MySQLConnection.")

        try:
            self._cnx_queue.put(cnx, block=False)
        except queue.Full:
            PoolError("Failed adding connection; queue is full")

    def add_connection(self, cnx=None):
        """Add a connection to the pool

        This method instantiates a Connection using the configuration
        passed when initializing the PyMySQLConnectionPool instance or using
        the set_config() method.
        If cnx is a Connection instance, it will be added to the
        queue.

        Raises PoolError when no configuration is set, when no more
        connection can be added (maximum reached) or when the connection
        can not be instantiated.
        """
        with CONNECTION_POOL_LOCK:
            if not self._cnx_config:
                raise PoolError("Connection configuration not available")

            if self._cnx_queue.full():
                raise PoolError("Failed adding connection; queue is full")

            if not cnx:
                cnx = Connection(**self._cnx_config)
                cnx._pool_config_version = self._config_version
            else:
                if not isinstance(cnx, Connection):
                    raise PoolError("Connection instance not subclass of MySQLConnection.")

            self._queue_connection(cnx)

    def get_connection(self):
        """Get a connection from the pool

        This method returns an PooledPyMySQLConnection instance which
        has a reference to the pool that created it, and the next available
        MySQL connection.

        When the MySQL connection is not connect, a reconnect is attempted.

        Raises PoolError on errors.

        Returns a PooledPyMySQLConnection instance.
        """
        with CONNECTION_POOL_LOCK:
            try:
                cnx = self._cnx_queue.get(block=False)
            except queue.Empty:
                raise PoolError("Failed getting connection; pool exhausted")

            if not is_connected(cnx) or self._config_version != cnx._pool_config_version:
                cnx = Connection(**self._cnx_config)
                try:
                    cnx.ping(reconnect=True)
                except Exception as e:
                    # Failed to reconnect, give connection back to pool
                    self._queue_connection(cnx)
                    raise
                cnx._pool_config_version = self._config_version

            return PooledPyMySQLConnection(self, cnx)

    def _remove_connections(self):
        """Close all connections

        This method closes all connections. It returns the number
        of connections it closed.

        Used mostly for tests.

        Returns int.
        """
        with CONNECTION_POOL_LOCK:
            cnt = 0
            cnxq = self._cnx_queue
            while cnxq.qsize():
                try:
                    cnx = cnxq.get(block=False)
                    cnx.close()
                    cnt += 1
                except queue.Empty:
                    return cnt
                except PoolError:
                    raise
                except Error:
                    # Any other error when closing means connection is closed
                    pass

            return cnt
