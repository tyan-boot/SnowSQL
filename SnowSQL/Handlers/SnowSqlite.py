from ..SnowSQL import ErrorConfig


class Sqlite3Handler(object):
    def __init__(self, db_config):
        self.__type = "sqlite3"
        # set placeholder
        self.placeholder = "?"
        self.escape = ''
        try:
            self.db_file = db_config["db_file"]
        except KeyError as e:
            raise ErrorConfig("Missing db_file in db_config")

        self.__db_con = None

    def connector(self):
        import sqlite3
        self.__db_con = sqlite3.connect(self.db_file)

    def exec(self, sql, content=None):
        if content is None:
            content = ()
        with self.__db_con as con:
            result = con.execute(sql, content)
            result = result.fetchall()
        return result

    def exec_one(self, sql, content=None):
        if content is None:
            content = ()
        with self.__db_con as con:
            result = con.execute(sql, content)
            result = result.fetchone()
        return result

    @property
    def tables(self):
        result = self.exec("select name from sqlite_master")
        __tables = []
        for t in result:
            __tables.append(t[0])
        return __tables
