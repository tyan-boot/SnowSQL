from ..SnowSQL import ErrorConfig


class MysqlHandler(object):
    def __init__(self, db_config):
        # get db info
        try:
            self.host = db_config["host"]
            self.user = db_config["user"]
            self.password = db_config["password"]
            self.db = db_config["database"]
        except KeyError as e:
            raise ErrorConfig("Lost %s in config" % e)

        if "charset" in db_config:
            self.charset = db_config["charset"]
        else:
            self.charset = "utf8"

        self.__db_con = None

    def connector(self):
        try:
            import pymysql
        except ModuleNotFoundError:
            raise ModuleNotFoundError("You must install pymysql first")
        else:
            self.__db_con = pymysql.connect(host=self.host,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            charset=self.charset,
                                            cursorclass=pymysql.cursors.DictCursor)

    def exec(self, sql, data=None):
        with self.__db_con.cursor() as cursor:
            cursor.execute(sql, data)
            self.__db_con.commit()
            result = cursor.fetchall()

        return result

    def exec_one(self, sql, data=None):
        with self.__db_con.cursor() as cursor:
            cursor.execute(sql, data)
            self.__db_con.commit()
            result = cursor.fetchone()

        return result

    @property
    def tables(self):
        result = self.exec("show tables")

        __tables = []
        for t in result:
            t = t.popitem()
            __tables.append(t[1])

        return __tables
