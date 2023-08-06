# pymysql_kits

pymysql_kits is a tool based on PyMySQL. It can quickly establish a database connection pool and conveniently execute SQL statements.

Contributing:
- The database connection pool module code comes from [mysql/mysql-connector-python](https://github.com/mysql/mysql-connector-python).
- The SQL statement operation code comes from [hopehook/python-lab](https://github.com/hopehook/python-lab/blob/master/data_tools/mysqllib.py).

## Requirements

- Python – one of the following:
    - CPython : 2.7 and >= 3.4
    - PyPy : Latest version
- MySQL Server – one of the following:
    - MySQL >= 5.5
    - MariaDB >= 5.5
- PyMySQL >= 0.8.1

## Installation

## Example

The following examples make use of a simple table

```SQL
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
```

### PyMySQLConnectionPool Demo

```Python
from pymysql_kits.pooling import PyMySQLConnectionPool

db_conf = {
    "host": "localhost",
    "user": "user",
    "password": "passwd",
    "database": "db",
    "port": 3306,
    "autocommit": True,
    "charset": "utf8mb4",
}

# Create connection pool
db_pool = PyMySQLConnectionPool(pool_size=5, pool_name='local_pool', **db_conf)

# Get a connection
connection = db_pool.get_connection()
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
```

### Connections and Transaction Demo

```python
from pymysql_kits import Connections

db_conf = {
    "host": "localhost",
    "user": "user",
    "password": "passwd",
    "database": "db",
    "port": 3306,
    "autocommit": True,
    "charset": "utf8mb4",
}

# Create a connection poll
conn = Connections(pool_size=5, **db_conf)

# Query
result = conn.fetchall("SELECT `id`, `password` FROM `users` WHERE `email`=%s", ('webmaster@python.org',))
print(result)

# Insert
conn.insert("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", ('webmaster@python.org', 'very-secret'))

# For transaction
transaction = conn.begin()
try:
    transaction.insert("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", ('webmaster@python.org', 'very-secret'))
except:
    transaction.rollback()
else:
    transaction.commit()
finally:
    transaction.close()

# or
with conn.begin() as transaction:
    transaction.insert("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", ('webmaster@python.org', 'very-secret'))

```

## License

pymysql_kits is released under the MIT License. See LICENSE for more information.