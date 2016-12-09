import re

from .SnowExceptions import ErrorConfig, ColumnNameError


class SnowSQLBase(object):
    def __init__(self, *, db_config):
        self.db_config = db_config
        if type(db_config) is not dict:
            raise ErrorConfig("配置错误")
        else:
            # check type info
            if "type" in db_config:
                if db_config["type"] == "sqlite":
                    self.__type = "sqlite"
                elif db_config["type"] == "mysql":
                    self.__type = "mysql"
                else:
                    raise TypeError("%s is not supported yet" % db_config["type"])
            else:
                raise ErrorConfig("缺少类型")

        # set placeholder
        self.placeholder = ""
        if self.__type == "sqlite":
            self.placeholder = "?"
        elif self.__type == "mysql":
            self.placeholder = "%s"

        # prepare regex
        self.__re_compare_symbol = re.compile("""([\w\.\-]+)(\[(<|>|!=|>=|<=)\])?""")

    def select_context(self, table, columns, where=None):
        content = []
        where_sql = ""
        if where is not None:
            __where = self.__where_case(where)
            where_sql = __where[0]
            content += __where[1]
        column_sql = ",".join(columns)

        select_sql = """SELECT %s FROM %s %s""" % (column_sql, table, where_sql)
        # print(select_sql)
        return select_sql, tuple(content)

    def insert(self, table, data):
        column = []
        values = []

        if type(data) is not dict:
            raise TypeError("Not a dict")
        else:
            for col, val in data.items():
                column.append(col)
                values.append(val)

            value_sql = "VALUE (" + ",".join([self.placeholder for x in range(0, len(column))]) + ")"
            column_sql = "(" + ",".join(column) + ") "

            insert_sql = """INSERT INTO %s""" % table + column_sql + value_sql
            return insert_sql, tuple(values)

    def update(self, table, data, where=None):
        sets = []
        values = []
        where_sql = ""
        if type(data) is not dict:
            raise TypeError("Not a dict")
        else:
            for col, val in data.items():
                set_sql = " %s=%s" % (col, self.placeholder)
                sets.append(set_sql)
                values.append(val)
                # print(sets)
            set_case = ",".join(sets)

            if where is not None:
                where_sql, content = self.__where_case(where=where)
                values += content
            return "UPDATE %s SET" % table + set_case + " " + where_sql, tuple(values)

        pass

    def has(self, table, where=None):
        sql, content = self.select_context(table, '*', where)
        return sql, content

    def count(self, table, where):
        sql, content = self.select_context(table, '*', where)
        return sql, content

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
                    tmp = self.__compare_parse(key)
                    where_sql = "%s%s%s" % (tmp[0], tmp[1], self.placeholder)
                    tmp = self.__case_parse(val, None)
                    if type(tmp) is list:
                        content = content + tmp
                    else:
                        content.append(tmp)
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
                    case_list.append("%s%s%s" % (col_name, compare_symbol, self.placeholder))
                    content.append(case_val)
                else:
                    # build placeholder in ()
                    placeholders = ((self.placeholder + ",") * len(case_val))[:-1]
                    if compare_symbol == "!=":
                        case_list.append("%s NOT IN (%s)" % (col_name, placeholders))
                    else:
                        case_list.append("%s IN (%s)" % (col_name, placeholders))

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
