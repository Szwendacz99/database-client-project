import logging

from src.database.datatypes import Datatype, check_data_type, convert
from src.exceptions import BadDatatypeException, TableException

log = logging.getLogger(__name__)


class Table:
    def __init__(self, name: str):
        """
        class for storing table, both structure and data
        """
        if name.strip() == "":
            raise TableException(name, additional_info="Inproper name of table")
        self.name = name

        # dictionary for storing names and types of columns
        # [(name, datatype)]
        self.columns = []
        # 2D table for storing rows data
        self.rows = []

    def get_columns_names(self) -> list:
        return [x[0] for x in self.columns]

    def add_column(self, col: tuple) -> None:
        """
        Add new column, and fill it with default value for
        its datatype if this table have any rows
        :param col: tuple (name, Datatype)
        :return:
        """
        name, datatype = col
        name = name.strip()
        if len(name.replace(" ", "")) == 0:
            raise TableException(self.name, additional_info="Name of column must have some letters")
        if name in self.get_columns_names():
            raise TableException(self.name, f"Column with name {name} already exists!")

        self.columns.append((name, datatype))

        for row in self.rows:
            if datatype in (Datatype.REAL, Datatype.ITEGER):
                row.append(0.0)
            else:
                row.append("")

    def insert_into_cell(self, column_index: int, item, row_reference: list) -> None:
        if check_data_type(item) != self.columns[column_index][1]:
            item = convert(item, self.columns[column_index][1])
        row_reference.append(item)

    def get_column_index(self, name: str) -> int:
        for i in range(len(self.columns)):
            if self.columns[i][0] == name:
                return i
        raise TableException(self.name, f"Cannot find index of not existing column \"{name}\"")

    def add_row(self, data: list):
        """
        add data to new row,
        throws BadDatatype, TableException on error, and then data
        is nt saved in table at all
        :param data: list of elements of new Row
        :return:
        """
        if len(data) != self.cols_num():
            raise TableException(self.name, "Inserted data dont match column amount of the table")
        new_row = []
        for i in range(self.cols_num()):
            self.insert_into_cell(i, data[i], new_row)
        self.rows.append(new_row)
        log.debug(f"To table {self.name} succesfully inserted data: {data}")

    def delete_row(self, index: int):
        self.rows.pop(index)

    def get(self, i, j):
        return self.rows[i][j]

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
