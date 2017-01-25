# SnowSQL
> Light Python database framework

# Features
* **Light** - only 40KB
* **Easy** - easy to learn and use
* **Compatible** - support Sqlite3 and Mysql/MariaDB
* **Security** - Prevent SQL injection

# Get Started

## Install
SnowSQL is developing and not fully finished, so you should install by youself.
``` shell
./setup.py bdist_wheel
cd dist
pip install *
```

## Connect to database
``` python

from SnowSQL import SnowSQL

# for mysql
# You must install pymysql first

db = SnowSQL(db_config={
     "type": "mysql"
     "host": "localhost",
     "user": "root",
     "password": "root",
     "database": "db",
     "charset": "utf8"
})

# for sqlite3

db = SnowSQL(db_config={
      "type": "sqlite3"
      "db_file": "sqlite3.db"
})

# select
result = db.select("table", ["col1", "col2"],
          where={
                    "AND": {
                        "col1[>]": 1,
                        "col2": 2,
                        }
                })

# insert 
db.insert("table", {
                        "col1": 1,
                        "col2": 2,
                        "col3": 3,
                    })


# update
db.update("table", { "col1": 1, "col2": 2 }, where={"col3[!=]": 3})

# delete
db.delete("table", { "col1": 1 })

# get - similar to select but return only one record
db.get("table", ["col1", "col2"], where={ "col3[>=]": 1 })

# has - return True when table contains "where", False when not
db.has("table", where={ "col1": 1})

# count
db.count("table")

# tables - get all tables name in database, in list format
tables = db.tables

```

# WHERE Syntax
## Basic
> WHERE is provided in dict, and it is easy to understand.

``` python
{
    "col1": "itsval"
}
# WHERE col1="itsval"

{
    "col1[>]": 1
}
# WHERE col1 >  1

{
    "col1[>=]": 1
}
# WHERE col1 >= 1

{
    "col1[!=]": 4
}
# WHERE col1 != 4

{
    "col1": [1, 2, 3]
}
# WHERE col1 IN (1, 2, 3)

{
    "col1[!=]": [1, 2, 3]
}
# WHERE col1 NOT IN (1, 2, 3)

```

## Relativity Syntax

``` python
{
    "AND": {
        "col1": 1,
        "col2": 2
    }
}
# WHERE col1 = 1 AND col2 = 2

{
    "OR":{
        "col1": 1,
        "col2": 2
    }
}
# WHERE col1 = 1 OR col2 =2

{
    "AND": {
        "OR": {
            "col1": 1,
            "col2": 2
        },
        "OR": {
            "col3": 3,
            "col4": 4
        }
    }
}
# WHERE (col1 = 1 OR col2 = 2) AND (col3 = 3 OR col4 = 4)

{
    "OR": {
        "AND": {
            "col1": 1,
            "col2": 2
        },
        "AND": {
            "col3": 3,
            "col4": 4
        }
    }
}
# WHERE (col1 = 1 AND col2 = 2) OR (col3 = 3 AND col4 = 4)

{
    "OR": {
        "AND": {
            "col1": 1,
            "col2": 2
        },
        "OR": {
            "col3": 3,
            "col4": 4
        }
    }
}
# WHERE (col1 = 1 AND col2 = 2) OR (col3 = 3 OR col4 = 4)
```

## Other Syntax
``` python
{
    "LIMIT": 10
}
# LIMIT 10

{
    "LIMIT": [3, 10]
}
# LIMIT 3, 10
```

# TODO
* JOIN Syntax
* ORDER
* GROUP
* LIKE
* MATCH
* SQL Functions
* Many execute
* Transaction

# Thanks
Inspired by Medoo
[medoo](http://medoo.in)
