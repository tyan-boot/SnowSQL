# SnowSQL
> Light Python database framework

# Features
* **Light** - only 20KB
* **Easy** - easy to learn and use
* **Compatible** - support Sqlite3 and Mysql/MariaDB
* **Security** - Prevent SQL injection

#Get Started

##Connect to database
```python

# for mysql

from SnowSQL_Mysql import SnowSQL

db = SnowSQL(db_config={
     "host": "localhost",
     "user": "root",
     "password": "root",
     "database": "db",
     "charset": "utf8"
})

# for sqlite3

from SnowSQL_Sqlite import SnowSQL

db = SnowSQL(db_config={
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
come up soon

```