import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QDialog, QGridLayout, QLineEdit, \
    QScrollArea, QComboBox

from src.database.datatypes import Datatype
from src.database.table import Table

log = logging.getLogger(__name__)


class NewTableDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.central_widget = None
        self.current_position = 0
        self.main_layout = None
        self.grid_layout = None

        self.result = None

        self.setup_ui()

    def setup_ui(self):
        """
        setup ui without showing it nor doing exec()
        main window have to do so
        :return:
        """
        log.debug("New table adding dialog creating...")
        self.resize(900, 900)
        self.main_layout = QGridLayout(self)
        self.grid_layout = QGridLayout(self)
        columns = QGroupBox(self)
        columns_scroll_box = QScrollArea(self)
        buttons_panel = QGroupBox(self)
        layout_buttons = QHBoxLayout()
        layout_buttons.setAlignment(Qt.AlignLeft)
        b_new_column = QPushButton("New Column")
        b_create_table = QPushButton("Create Table")
        layout_buttons.addWidget(b_new_column)

        layout_buttons.addWidget(b_create_table)
        buttons_panel.setLayout(layout_buttons)

        self.main_layout.addWidget(buttons_panel, 0, 0, 1, 10)
        columns.setLayout(self.grid_layout)
        columns_scroll_box.setWidget(columns)
        columns_scroll_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        columns_scroll_box.setWidgetResizable(True)
        self.main_layout.addWidget(columns_scroll_box, 1, 0, 9, 10)
        self.setLayout(self.main_layout)

        b_new_column.clicked.connect(self.add_new_column)
        b_create_table.clicked.connect(self.create_table)
        self.add_new_column()

        self.setWindowTitle('New table')
        log.debug("New table adding dialog created")

    def add_new_column(self):
        log.debug("New column widgets creating....")
        name = QLineEdit(self)
        name.setText("column name")
        self.grid_layout.addWidget(name, self.current_position, 0, 1, 7)
        combo = QComboBox(self)
        combo.addItem(Datatype.ITEGER.value, Datatype.ITEGER)
        combo.addItem(Datatype.REAL.value, Datatype.REAL)
        combo.addItem(Datatype.STRING.value, Datatype.STRING)
        self.grid_layout.addWidget(combo, self.current_position, 7, 1, 3)
        self.current_position += 1

    def get_columns(self):
        columns = []
        for i in range(0, self.current_position):
            name = self.grid_layout.itemAtPosition(i, 0)
            datatype = self.grid_layout.itemAtPosition(i, 9)
            columns.append((name.widget().text(), datatype.widget().itemData(datatype.widget().currentIndex())))
        return columns

    def create_table(self):
        columns = self.get_columns()
        table = Table("Test name")
        for col in columns:
            table.add_column(col)
        self.result = table
        self.accept()
