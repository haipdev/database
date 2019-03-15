# haip.config

[![License](https://img.shields.io/github/license/haipdev/database.svg)](LICENSE)
[![Build Status](https://travis-ci.org/haipdev/database.svg?branch=master)](https://travis-ci.org/haipdev/database)

haip.database is a minimalistic async database interface for Python 3

** ALPHA version **

## Features

* **minimalistic**: *query* and *do*
* **db by name**: reference your database (sessions) per config-name
* **sql templates**: SQL seperated from code. placeholders are escaped automatically.
* **db pools**: db connection pooling
* **dict short notation**: row.fieldname == row['fieldname']
* **db supported**: mysql, oracle, mssql, (ongoing)

## Getting Started

### Installing

upcoming:

```sh
pip install haip-database
```

currently only installation from source is possible

or from source:

```sh
git clone https://github.com/haipdev/database.git
```

### Usage

#### Config-files

```yaml
databases:
    mysql_test_db:
        type: mysql
        host: host
        port: port
        database: database
        username: username
        password: password
        max_connections: 3
        max_idle_connections: 3

    oracle_test_db:
        type: oracle
        host: host
        port: port
        username: username
        password: password
        service_name: service_name

    mssql_test_db:
        type: mssql
        driver: driver
        host: host
        port: port
        database: TEST
        username: username
        password: password
```

The database is identified by the section-name (e.g. 'mysql_test_db').

##### Common options

* **type**: mysql | oracle
* **host**: hostname/IP of the database server - default='127.0.0.1'
* **port**: port the database server is listening at - default depends on the type (mysql=3306, oracle=1521)
* **username**: username for login
* **password**: password for login
* **autocommit**: true | false - default=true
* **max_connections**: max number of open connections for this database (otherwise you will get DatabasePoolExhaustedExcpetions)
* **max_idle_connections**: max number of open idle connections

##### Mysql options

* **database**: name of the database on the database-server

##### Oracle options

* **service_name**: service-name (higher priority then SID)
* **sid**: sid

##### MSSQL options

* **driver**: driver definition string e.g. ""{SQL Server}"

##### Example

/path-to-my-config-dir/databases.yml

```yaml
databases:
    testdb:
        type: mysql
        username: testuser
        host: 127.0.0.2
```

(optionally you can place e.g. the passwords in seperate files):

/path-to-my-config-dir/dev/databases.yml

```yaml
databases:
    testdb:
        password: testpassword
```

#### Functions

#### Query

> async def query(db_name, query_template, *values, **args)

* *db_name*: the name of the database as defined in the configuration files (main section "databases" - in the example above e.g. "testdb")
* *query_template*: the filename of the template-file containing the SQL query. This file must have the suffix ".sql".
* **values*: values for query placeholders
* ***args*: the template-vars for the query_template jinja template.

This function returns an array of arrays (array of rows).

##### Query example

/path-to-my-config-dir/queries/firstname.sql

```sql
SELECT firstname, lastname
    FROM users
    WHERE firstname = '{{ firstname }}
```

```python
import haip.config as config
import haip.database as database

config.load('/path-to-my-config-dir', 'dev')
rows = await database.query('testdb', 'queries/firstname.sql', firstname='Reinhard')

for row in rows:
    firstname = row[0]
    lastname = row[1]
```

##### shortcuts

> async def query_assoc(db_name, query_template, **args)

Like "query" but returns an array of dicts. e.g. rows[0]['firstname'] or rows[0].firstname

> async def query_first(db_name, query_template, **args)

Like "query" but returns only the first row as dict. e.g. row['firstname'] or row.firstname. If no rows found None will be returned.

#### Insert/Updates

> async def do(db_name, query_template, **args)

Arguments like "query". This function returns the number of rows effected by this statement.

##### Do example

/path-to-my-config-dir/queries/update.sql

```sql
UPDATE users
    SET firstname='Test'
WHERE lastname = '{{ lastname }}
```

```python
import haip.config as config
import haip.database as database

config.load('/path-to-my-config-dir', 'dev')
changes = await database.do('testdb', 'queries/update.sql', lastname='Hainz')

print(f'effected rows: {changes}')
```

#### Procedures

> async def call(db_name, procedure)

* *db_name*: as above
* *procedure*: the name of the procedure to be called

## Running the tests

Tests are written using pytest and located in the "tests" directory.

```sh
pytest tests
```

## Contributing

Feel free to use and enhance this project. Pull requests are welcome.

## Authors

* **Reinhard Hainz** - *Initial work* - [haipdev](https://github.com/haipdev)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Dependencies

* [haip_config](https://github.com/haipdev/config)
* [haip_template](https://github.com/haipdev/template)
