import pymysql
import pymysql.cursors

from . import SnowSQLBase
from SnowSQL import ErrorConfig, ColumnNameError


class SnowSQL(SnowSQLBase):
    def __init__(self, db_config):
        db_config["type"] = "mysql"
        super(SnowSQL, self).__init__(db_config=db_config)

        try:
            host = db_config["host"]
            user = db_config["user"]
            password = db_config["password"]
            db = db_config["database"]
        except KeyError as e:
            raise ErrorConfig("Lost %s in config" % e)

        if "charset" in db_config:
            charset = db_config["charset"]
        else:
            charset = "utf8"

        self.__db_con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset,
                                        cursorclass=pymysql.cursors.DictCursor)

    def __exec(self, sql, data=None):
        with self.__db_con.cursor() as cursor:
            cursor.execute(sql, data)
            self.__db_con.commit()
            result = cursor.fetchall()

        return result

    def __exec_one(self, sql, data=None):
        with self.__db_con.cursor() as cursor:
            cursor.execute(sql, data)
            self.__db_con.commit()
            result = cursor.fetchone()

        return result

    def select(self, table, columns, where=None):
        sql, content = super(SnowSQL, self).select_context(table, columns, where)
        return self.__exec(sql, tuple(content))

    def insert(self, table, data):
        sql, content = super(SnowSQL, self).insert(table, data)
        return self.__exec(sql, content)

    def update(self, table, data, where=None):
        sql, content = super(SnowSQL, self).update(table, data, where)
        return self.__exec(sql, content)

    def delete(self, table, where):
        pass

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

    def count(self, table, where=None):
        sql, content = super(SnowSQL, self).count(table, where)
        result = self.__exec(sql, content)
        return len(result)

    def query(self, sql, content):
        return self.__exec(sql, content)
