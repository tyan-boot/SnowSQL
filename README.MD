# SnowSQL
> Light Python database framework

# Features
* **Light** - only 40KB
* **Easy** - easy to learn and use
* **Compatible** - support Sqlite3 and Mysql/MariaDB
* **Security** - Prevent SQL injection

#Get Started

##Connect to database
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