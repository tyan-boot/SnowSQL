class ErrorConfig(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass


class ColumnNameError(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass
