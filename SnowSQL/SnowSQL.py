import re

from .SnowExceptions import ErrorConfig, ColumnNameError


class SnowSQL(object):
    def __init__(self, *, db_config):
        self.db_config = db_config
        if type(db_config) is not dict:
            raise ErrorConfig("配置错误")
        else:
            # check type info
            if "type" in db_config:
                if db_config["type"] == "sqlite3":
                    self.__type = "sqlite3"
                    # set placeholder
                    self.placeholder = "?"
                    self.escape = ''

                    from .Handlers import SnowSqlite

                    self.__handler = SnowSqlite.Sqlite3Handler(db_config)

                elif db_config["type"] == "mysql":
                    self.__type = "mysql"
                    self.placeholder = "%s"
                    self.escape = '`'

                    from .Handlers import SnowMysql

                    self.__handler = SnowMysql.MysqlHandler(db_config)

                else:
                    raise TypeError("%s is not supported yet" % db_config["type"])
            else:
                raise ErrorConfig("缺少类型")

        # prepare regex
        self.__re_compare_symbol = re.compile("""([\w\.\-]+)(\[(<|>|!=|>=|<=)\])?""")

        # connect to database
        self.__handler.connector()

    def select(self, table, columns, where=None):
        """
        select
        :param table: the table to select, in string
        :param columns: "*" or a list: ["col1", "col2"]
        :param where:
        :return: a dict list contain data
        """

        sql, content = self.select_context(table, columns, where)
        return self.__handler.exec(sql, content)

    def insert(self, table, data):
        """
        insert
        :param table: the table to insert, in string
        :param data: data, in dict
        :return:
        """
        sql, content = self.__insert(table, data)
        return self.__handler.exec(sql, content)

    def update(self, table, data, where=None):
        """
        update
        :param table: the table to update
        :param data: date, in dict
        :param where:
        :return:
        """
        sql, content = self.__update(table, data, where)
        return self.__handler.exec(sql, content)

    def delete(self, table, where=None):
        """
        delete
        :param table: the table to delete
        :param where:
        :return:
        """
        sql, content = self.__delete(table, where)
        return self.__handler.exec_one(sql, content)

    def get(self, table, columns, where=None):
        """
        get single data instead of select all
        :param table: the table to get
        :param columns: "*" or list, same as select
        :param where:
        :return: a dict
        """
        sql, content = self.select_context(table, columns, where)
        return self.__handler.exec_one(sql, content)

    def has(self, table, where=None):
        """
        where a table contains something filter by where
        :param table: the table to find
        :param where:
        :return: boolean
        """
        sql, content = self.__has(table, where=where)
        result = self.__handler.exec_one(sql, content)
        if result is None:
            return False
        else:
            return True

    def count(self, table):
        """
        count
        :param table: the table to count
        :return: amount in int
        """
        sql = self.__count(table)
        result = self.__handler.exec_one(sql, None)
        if self.__type == "mysql":
            return result["count"]
        elif self.__type == "sqlite3":
            return result[0]

    def query(self, sql, content=None):
        """
        execute a raw sql
        :param sql: sql with placeholder
        :param content: tuple to fit placeholder
        :return: mixed
        """
        return self.__handler.exec(sql, content)

    def select_context(self, table, columns, where=None):
        content = []
        where_sql = ""
        if where is not None:
            __where = self.__where_case(where)
            where_sql = __where[0]
            content += __where[1]
        if type(columns) is list:
            column_sql = ",".join(self.__column_escape(columns))
        else:
            if columns != "*":
                column_sql = self.__column_escape(columns)
            else:
                column_sql = "*"

        select_sql = """SELECT %s FROM %s %s""" % (column_sql, table, where_sql)
        return select_sql, tuple(content)

    def __insert(self, table, data):
        column = []
        values = []

        if type(data) is not dict:
            raise TypeError("Not a dict")
        else:
            for col, val in data.items():
                column.append(col)
                values.append(val)

            value_sql = "VALUES (" + ",".join([self.placeholder for x in range(0, len(column))]) + ")"
            column_sql = "(" + ",".join(self.__column_escape(column)) + ") "

            insert_sql = """INSERT INTO %s""" % table + column_sql + value_sql
            return insert_sql, tuple(values)

    def __update(self, table, data, where=None):
        sets = []
        values = []
        where_sql = ""
        if type(data) is not dict:
            raise TypeError("Not a dict")
        else:
            for col, val in data.items():
                set_sql = " %s=%s" % (self.__column_escape(col), self.placeholder)
                sets.append(set_sql)
                values.append(val)
            set_case = ",".join(sets)

            if where is not None:
                where_sql, content = self.__where_case(where=where)
                values += content
            return "UPDATE %s SET" % table + set_case + " " + where_sql, tuple(values)

        pass

    def __delete(self, table, where=None):
        if type(where) is not dict:
            raise TypeError("Not a dict")
        else:
            where_sql, content = self.__where_case(where)
            return "DELETE FROM %s " % table + where_sql, content

    def __has(self, table, where=None):
        sql, content = self.select_context(table, '*', where)
        return sql, content

    def __count(self, table):
        return "SELECT COUNT(*) AS count FROM %s" % table

    @property
    def tables(self):
        return self.__handler.tables

    """
        build where case sql
    """

    def __where_case(self, where):

        if type(where) is not dict:
            pass
        else:
            where_sql = ""
            content = []
            limit_sql = ""
            for key, val in where.items():
                if key == "AND":
                    connector = "AND"
                elif key == "OR":
                    connector = "OR"
                elif key == "LIMIT":
                    limit_sql = " LIMIT " + ",".join(list(map(str, val)))
                    continue
                else:
                    connector = None

                if connector in ("AND", "OR"):
                    part = self.__case_parse(val, connector)
                    where_sql = where_sql + " " + part[0]
                    content = content + part[1]
                else:
                    col_name, compare_symbol = self.__compare_parse(key)

                    if type(val) is list:
                        placeholders = ((self.placeholder + ",") * len(val))[:-1]
                        if compare_symbol == "!=":
                            where_sql = "%s NOT IN (%s)" % (self.__column_escape(col_name), placeholders)
                        else:
                            where_sql = "%s IN (%s)" % (self.__column_escape(col_name), placeholders)
                        content += val
                    else:
                        where_sql = "%s%s%s" % (self.__column_escape(col_name), compare_symbol, self.placeholder)
                        content.append(val)
            if where_sql == "":
                return limit_sql, content
            else:
                return "WHERE " + where_sql + limit_sql, content

    def __case_parse(self, case, connector, content=None):
        if content is None:
            content = []

        # make sure case is not a list to use >, <, = etc.
        if type(case) is dict:
            case_list = []
            for case_key, case_val in case.items():
                # inner case
                if case_key is "AND" or case_key is "OR":
                    # now the case_key is the new connector
                    inner_case = self.__case_parse(case_val, case_key)
                    case_list.append("(" + inner_case[0] + ")")
                    content = content + inner_case[1]
                    continue

                # this is a list and should use IN or NOT IN
                if type(case_val) is list:
                    in_list = self.__case_parse(case_val, connector)
                    # and i append its contents into the whole contents
                    content = content + case_val
                else:
                    in_list = None

                (col_name, compare_symbol) = self.__compare_parse(case_key)
                if in_list is None:
                    if case_val is "NULL" or case_val is "null":
                        case_list.append("%s%sNULL" % (self.__column_escape(col_name), compare_symbol))
                    else:
                        case_list.append("%s%s%s" % (self.__column_escape(col_name), compare_symbol, self.placeholder))
                        content.append(case_val)
                else:
                    # build placeholder in ()
                    placeholders = ((self.placeholder + ",") * len(case_val))[:-1]
                    if compare_symbol == "!=":
                        case_list.append("%s NOT IN (%s)" % (self.__column_escape(col_name), placeholders))
                    else:
                        case_list.append("%s IN (%s)" % (self.__column_escape(col_name), placeholders))

            where_sql = (" " + connector + " ").join(case_list)
            return where_sql, content
        elif type(case) is list:
            return ",".join(map(str, case))
        else:
            return case

    def __compare_parse(self, col_key):
        # check compare symbol
        matches = self.__re_compare_symbol.search(col_key)
        if matches is None:
            raise ColumnNameError("Column name error")
        else:
            if matches.group(1) is None:
                raise ColumnNameError("Cannot find column name")
            else:
                col_name = matches.group(1)
                if matches.group(3) is not None:
                    compare_symbol = matches.group(3)
                else:
                    compare_symbol = "="

            return col_name, compare_symbol

    def __column_escape(self, columns):
        if type(columns) is list:
            columns_escaped = []
            for col in columns:
                columns_escaped.append("%s%s%s" % (self.escape, col, self.escape))
            return columns_escaped
        else:
            return "%s%s%s" % (self.escape, columns, self.escape)
