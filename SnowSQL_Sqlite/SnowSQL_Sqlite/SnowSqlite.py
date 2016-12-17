import sqlite3

from . import SnowSQLBase
from SnowSQL import ErrorConfig, ColumnNameError


class SnowSQL(SnowSQLBase):
    def __init__(self, *, db_config):
        db_config["type"] = "sqlite"
        super(SnowSQL, self).__init__(db_config=db_config)

        try:
            file = db_config["db_file"]
        except KeyError as e:
            raise ErrorConfig("Config error, no %s found" % e)

        self.__db_con = sqlite3.connect(file)

    def __exec(self, sql, content):
        with self.__db_con.cursor() as cursor:
            r = cursor.execute(sql, content)
            self.__db_con.commit()
            r = r.fetchall()
        return r

    def __exec_one(self, sql, content):
        with self.__db_con.cursor() as cursor:
            r = cursor.execute(sql, content)
            self.__db_con.commit()
            r = r.fetchone()
        return r

    def select(self, table, columns, where=None):
        sql, content = super(SnowSQL, self).select_context(table, columns, where)
        return self.__exec(sql, content)

    def insert(self, table, data):
        sql, content = super(SnowSQL, self).insert(table, data)
        return self.__exec(sql, content)

    def update(self, table, data, where=None):
        sql, content = super(SnowSQL, self).update(table, data, where)
        return self.__exec(sql, content)

    def delete(self, table, where=None):
        sql, content = super(SnowSQL, self).delete(table, where)
        return self.__exec_one(sql, content)

    def get(self, table, columns, where=None):
        sql, content = super(SnowSQL, self).select_context(table, columns, where)
        return self.__exec_one(sql, tuple(content))

    def has(self, table, where=None):
        sql, content = super(SnowSQL, self).has(table, where=where)
        result = self.__exec_one(sql, content)
        if result is None:
            return False
        else:
            return True

    def count(self, table):
        sql = super(SnowSQL, self).count(table)
        result = self.__exec(sql, None)
        return result[0]["count"]

    def close(self):
        self.__db_con.close()
