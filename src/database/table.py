from src.database.datatypes import Datatype, check_data_type
from src.exceptions import BadDatatype, TableException
import src.settings as settings


class Table:
    def __init__(self, name):
        """
        class for storing table, both structure and data
        """
        self.name = name

        # 2D table for storing names and types of columns
        # {index: (name, datatype)}
        self.columns = {}
        # 2D table for storing rows data
        self.rows = []

    def add_column(self, name: str, datatype: Datatype) -> bool:
        """
        Add new columnt, and fill it with default value for
        its datatype if this table have any rows
        :param name:
        :param datatype:
        :return:
        """
        if len(name.replace(" ", "")) == "":
            return False
        self.columns[self.cols_num()] = (name, datatype)

        for row in self.rows:
            if datatype in (Datatype.REAL, Datatype.ITEGER):
                row[self.cols_num()-1] = 0.0
            else:
                row[self.cols_num()-1] = ""

    def insert_into_cell(self, column_index: int, item, row_reference: list) -> None:
        if check_data_type(item) != self.columns[column_index][1]:
            raise BadDatatype(f"Cannot insert {type(item).__name__} into {self.columns[column_index][0]} "
                              f"column in table {self.name}, proper type: {self.columns[column_index][1]}")
        row_reference[column_index] = item

    def add_row(self, *args):
        if len(args) != self.cols_num():
            raise TableException(self.name, "Inserted data dont match column amount of the table")
        new_row = []
        for i in range(self.cols_num()):
            self.insert_into_cell(i, args[i], new_row)
        self.rows.append(new_row)
        settings.debug(f"To table {self.name} succesfully inserted data: {args}")

    def cols_num(self) -> int:
        """
        :return: number of columns in this table
        """
        return len(self.columns)

    def rows_num(self) -> int:
        """
        :return: number of rows in this table
        """
        return len(self.rows)
