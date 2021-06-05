import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QGroupBox, QScrollArea, QGridLayout, QLineEdit, \
    QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox

from src.database.table import Table
from src.exceptions import ClientException

log = logging.getLogger(__name__)


def isfloat(str: str):
    try:
        float(str)
        return True
    except ValueError:
        return False


class SearchDialog(QDialog):

    def __init__(self, table: Table):
        super().__init__()

        self.central_widget = None
        self.current_position = 0
        self.main_layout = None
        self.grid_layout = None
        self.input = None
        self.tabs = None
        self.table = table

        self.setup_ui()

    def setup_ui(self):
        """
        setup ui without showing it nor doing exec()
        main window have to do so
        :return:
        """
        log.debug("New search dialog creating...")
        self.resize(900, 900)
        self.main_layout = QGridLayout(self)
        self.grid_layout = QGridLayout(self)
        self.tabs = QTabWidget(self)
        buttons_panel = QGroupBox(self)
        layout_buttons = QHBoxLayout()
        layout_buttons.setAlignment(Qt.AlignLeft)
        b_search = QPushButton("Search")

        layout_buttons.addWidget(b_search)
        buttons_panel.setLayout(layout_buttons)

        self.input = QLineEdit(self)
        self.input.setText("lambda row: row[\"wzrost\"]>1.9")
        self.main_layout.addWidget(self.input, 0, 0, 1, 7)

        self.main_layout.addWidget(buttons_panel, 0, 7, 1, 3)

        self.main_layout.addWidget(self.tabs, 1, 0, 9, 10)
        self.setLayout(self.main_layout)

        b_search.clicked.connect(self.search_start)

        self.setWindowTitle(f'Searching in table "{self.table.name}"')
        log.debug("Search dialog created")

    def display_result(self, table: Table):
        table_widget = QTableWidget()
        table_widget.setRowCount(table.rows_num())
        table_widget.setColumnCount(table.cols_num())
        for i, name in zip(range(table.cols_num()), table.get_columns_names()):
            table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(name))
        for i in range(table.rows_num()):
            for j in range(table.cols_num()):
                table_widget.setItem(i, j, QTableWidgetItem(f"{table.get(i, j)}"))
        self.tabs.addTab(table_widget, table.name)
        self.tabs.setCurrentIndex(self.tabs.count()-1)

    def show_error_dialog(self, error: ClientException):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Cannot create table")
        msg.setInformativeText(str(error))
        msg.setWindowTitle("Error")
        msg.show()

    def search_start(self):
        try:
            query = self.input.text().split(":", 1)[1]
            query = query.replace("row[\"", "")
            query = query.replace("\"]", "")
            rows = []
            for row in self.table.rows:
                if self.check(query, row):
                    rows.append(row)
            result = Table("Result")
            result.columns = self.table.columns
            result.rows = rows
            self.display_result(result)
        except ClientException as e:
            self.show_error_dialog(e)
            return

    def check(self, query: str, row: list) -> bool:
        query = query.strip()
        if len(query.split(" or ")) > 1:
            parts = query.split(" or ", 1)
            return self.check(parts[0], row) or self.check(parts[1], row)
        elif len(query.split(" and ")) > 1:
            parts = query.split(" and ", 1)
            return self.check(parts[0], row) and self.check(parts[1], row)
        elif ">" in query:
            parts = query.split(">", 1)
            part1 = parts[0].strip()
            part2 = parts[1].strip()
            if isfloat(part1) and not isfloat(part2):
                part1 = float(part1)
                col_index = self.table.get_column_index(part2)
                return part1 > row[col_index]
            elif not isfloat(part1) and isfloat(part2):
                col_index = self.table.get_column_index(part1)
                part2 = float(part2)
                return row[col_index] > part2
            elif not isfloat(part1) and not isfloat(part2):
                col_index1 = self.table.get_column_index(part1)
                col_index2 = self.table.get_column_index(part2)
                return row[col_index1] > row[col_index2]
            elif isfloat(part1) and isfloat(part2):
                part1 = float(part1)
                part2 = float(part2)
                return part1 > part2
        elif "<" in query:
            parts = query.split("<", 1)
            part1 = parts[0].strip()
            part2 = parts[1].strip()
            if isfloat(part1) and not isfloat(part2):
                part1 = float(part1)
                col_index = self.table.get_column_index(part2)
                return part1 < row[col_index]
            elif not isfloat(part1) and isfloat(part2):
                col_index = self.table.get_column_index(part1)
                part2 = float(part2)
                return row[col_index] < part2
            elif not isfloat(part1) and not isfloat(part2):
                col_index1 = self.table.get_column_index(part1)
                col_index2 = self.table.get_column_index(part2)
                return row[col_index1] < row[col_index2]
            elif isfloat(part1) and isfloat(part2):
                part1 = float(part1)
                part2 = float(part2)
                return part1 < part2
        elif "==" in query:
            parts = query.split("==", 1)
            part1 = parts[0].strip()
            part2 = parts[1].strip()
            if isfloat(part1) and not isfloat(part2):
                part1 = float(part1)
                col_index = self.table.get_column_index(part2)
                return part1 == row[col_index]
            elif not isfloat(part1) and isfloat(part2):
                col_index = self.table.get_column_index(part1)
                part2 = float(part2)
                return row[col_index] == part2
            elif not isfloat(part1) and not isfloat(part2):
                col_index1 = self.table.get_column_index(part1)
                col_index2 = self.table.get_column_index(part2)
                return row[col_index1] == row[col_index2]
            elif isfloat(part1) and isfloat(part2):
                part1 = float(part1)
                part2 = float(part2)
                return part1 == part2
        raise ClientException(f"Your query is bad, check what is wrong with \"{query}\"")
