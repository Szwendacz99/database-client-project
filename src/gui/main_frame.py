import logging
from PyQt5.QtWidgets import QListWidget, QMainWindow, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, \
    QDockWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

from src.database.database import Database
from src.database.table import Table
from src.gui.newtabledialog import NewTableDialog

log = logging.getLogger(__name__)


class MainFrame(QMainWindow):

    def __init__(self):
        """
        Main Window class
        """
        super().__init__()

        self.database = Database()

        self.central_widget = None
        self.tabs = None
        self.table_list = None
        self.table_list_dockable = None

        self.setup_ui()

    def setup_ui(self):
        """
        Create main window
        :return: None
        """
        log.debug("Setting up GUI....")
        self.resize(1200, 900)

        self.create_central_widget()
        self.create_docking_tables_list_panel()

        self.setWindowTitle('Database Client')
        self.show()

    def create_central_widget(self):
        """
        create central widget with tables chosing widget on the left
        and QTabWidget for main display in the center/right
        :return: None
        """
        log.debug("Creating central widget....")
        self.central_widget = QGroupBox(self)
        self.central_widget.setContentsMargins(5, 5, 5, 5)
        layout = QGridLayout()

        box = QGroupBox(self)
        layout_buttons = QHBoxLayout()
        layout_buttons.setAlignment(Qt.AlignLeft)

        b_add_table = QPushButton("Add new table")
        b_add_table.clicked.connect(self.add_new_table)
        layout_buttons.addWidget(b_add_table, alignment=Qt.AlignLeft)

        b_close_table = QPushButton("Close table")
        b_close_table.clicked.connect(self.close_table)
        layout_buttons.addWidget(b_close_table, alignment=Qt.AlignLeft)

        box.setLayout(layout_buttons)
        layout.addWidget(box, 0, 0, 4, 10)

        self.tabs = QTabWidget(self.central_widget)

        layout.addWidget(self.tabs, 4, 0, 100, 10)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def create_docking_tables_list_panel(self):
        """
        Create docking widget with sorted list of tables
        :return: None
        """
        self.table_list_dockable = QDockWidget("Tables", self)
        self.table_list = QListWidget(self.central_widget)
        self.table_list.setSortingEnabled(True)
        self.table_list_dockable.setWidget(self.table_list)
        self.table_list.doubleClicked.connect(self.show_selected_tables)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.table_list_dockable)

    def update_table_list(self):
        table_list = self.database.list_tables_names()
        self.table_list.clear()
        for name in table_list:
            self.table_list.addItem(name)

    def add_new_table(self):
        dialog = NewTableDialog()
        # dialog.show()
        dialog.exec()
        if dialog.result is not None:
            self.database.add_table(dialog.result)
            self.update_table_list()

    def show_table(self, table: Table):
        table_widget = QTableWidget()
        table_widget.setRowCount(table.rows_num())
        table_widget.setColumnCount(table.cols_num())
        for i, name in zip(range(table.cols_num()), table.get_columns_names()):
            table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(name))
        for i in range(table.cols_num()):
            for j in range(table.rows_num()):
                table_widget.setItem(i, j, QTableWidgetItem(f"{table.get(i, j)}"))
        self.tabs.addTab(table_widget, table.name)

    def show_selected_tables(self):
        table_names = [item.text() for item in self.table_list.selectedItems()]
        for name in table_names:
            table = self.database.get_table(name)
            self.show_table(table)

    def close_table(self):
        self.tabs.removeTab(self.tabs.currentIndex())
