class ClientException(Exception):
    def __init__(self, error_info="Unknown error of client application!"):
        self.error_info = error_info

    def __str__(self):
        return f"{type(self).__name__}: {self.error_info}"


class TableException(ClientException):
    def __init__(self, table_name, additional_info=""):
        self.table_name = table_name
        self.error_info = f"Error in {table_name} table! {additional_info}"


class BadDatatype(ClientException):
    def __init__(self, error_info="Bad datatype!"):
        self.error_info = error_info
