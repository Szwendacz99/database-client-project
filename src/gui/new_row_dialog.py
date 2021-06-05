import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QDialog, QGridLayout, QLineEdit, \
    QScrollArea, QComboBox, QMessageBox, QLabel

from src.database.datatypes import Datatype
from src.database.table import Table
from src.exceptions import ClientException

log = logging.getLogger(__name__)


class NewRowDialog(QDialog):

    def __init__(self, table: Table):
        super().__init__()

        self.central_widget = None
        self.current_position = 0
        self.main_layout = None
        self.grid_layout = None
        self.table_name_input = None
        self.result = None
        self.table = table

        self.setup_ui()

    def setup_ui(self):
        """
        setup ui without showing it nor doing exec()
        main window have to do so
        :return:
        """
        log.debug("New row adding dialog creating...")
        self.resize(900, 900)
        self.main_layout = QGridLayout(self)
        self.grid_layout = QGridLayout(self)
        columns = QGroupBox(self)
        columns_scroll_box = QScrollArea(self)
        buttons_panel = QGroupBox(self)
        layout_buttons = QHBoxLayout()
        layout_buttons.setAlignment(Qt.AlignLeft)
        b_insert = QPushButton("Insert this data to table")

        layout_buttons.addWidget(b_insert)
        buttons_panel.setLayout(layout_buttons)

        self.main_layout.addWidget(buttons_panel, 0, 0, 1, 10)
        columns.setLayout(self.grid_layout)
        columns_scroll_box.setWidget(columns)
        columns_scroll_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        columns_scroll_box.setWidgetResizable(True)
        self.main_layout.addWidget(columns_scroll_box, 1, 0, 9, 10)
        self.setLayout(self.main_layout)

        b_insert.clicked.connect(self.insert)

        for column in self.table.get_columns_names():
            self.add_new_column(column)

        self.setWindowTitle(f'New row in table "{self.table.name}"')
        log.debug("New row adding dialog created")

    def add_new_column(self, column_name: str):
        log.debug("New column input widgets creating....")
        name = QLabel(self)
        name.setText(column_name)
        self.grid_layout.addWidget(name, self.current_position, 0, 1, 3)
        input_field = QLineEdit(self)
        self.grid_layout.addWidget(input_field, self.current_position, 3, 1, 7)
        self.current_position += 1

    def get_row_data(self):
        columns = []
        for i in range(0, self.current_position):
            data = self.grid_layout.itemAtPosition(i, 9)
            columns.append(data.widget().text())
        return columns

    def show_error_dialog(self, error: ClientException):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Cannot create table")
        msg.setInformativeText(str(error))
        msg.setWindowTitle("Error")
        msg.show()

    def insert(self):
        try:
            data = self.get_row_data()
            self.table.add_row(data)
        except ClientException as e:
            self.show_error_dialog(e)
