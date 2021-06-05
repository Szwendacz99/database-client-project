import logging
from PyQt5.QtWidgets import QListWidget, QMainWindow, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, \
    QDockWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

from src.database.database import Database
from src.database.table import Table
from src.gui.new_row_dialog import NewRowDialog
from src.gui.new_table_dialog import NewTableDialog

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

        b_delete_table = QPushButton("Delete table")
        b_delete_table.clicked.connect(self.delete_table)
        layout_buttons.addWidget(b_delete_table, alignment=Qt.AlignLeft)

        b_new_row = QPushButton("Add new row")
        b_new_row.clicked.connect(self.add_new_row)
        layout_buttons.addWidget(b_new_row, alignment=Qt.AlignLeft)

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
        dialog.exec()
        if dialog.result is not None:
            self.database.add_table(dialog.result)
            self.update_table_list()

    def check_if_table_open(self, name: str):
        for i in range(self.tabs.count()):
            if name == self.tabs.tabText(i):
                return True
        return False

    def show_table(self, table: Table):
        if self.check_if_table_open(table.name):
            return
        table_widget = QTableWidget()
        table_widget.setRowCount(table.rows_num())
        table_widget.setColumnCount(table.cols_num())
        for i, name in zip(range(table.cols_num()), table.get_columns_names()):
            table_widget.setHorizontalHeaderItem(i, QTableWidgetItem(name))
        for i in range(table.rows_num()):
            for j in range(table.cols_num()):
                table_widget.setItem(i, j, QTableWidgetItem(f"{table.get(i, j)}"))
        self.tabs.addTab(table_widget, table.name)

    def show_selected_tables(self):
        table_names = [item.text() for item in self.table_list.selectedItems()]
        for name in table_names:
            table = self.database.get_table(name)
            self.show_table(table)

    def close_table(self):
        log.debug(f"closig view of currently opened tab with index {self.tabs.currentIndex()}")
        self.tabs.removeTab(self.tabs.currentIndex())

    def add_new_row(self):
        if self.tabs.currentIndex() == -1:
            return
        name = self.tabs.tabText(self.tabs.currentIndex())
        table = self.database.get_table(name)
        dialog = NewRowDialog(table)
        dialog.exec()
        self.refresh_view()

    def refresh_view(self):
        log.debug("Refreshing opened tabs view")
        opened_tabs = []
        current_opened_index = self.tabs.currentIndex()
        for i in range(self.tabs.count()):
            opened_tabs.append(self.tabs.tabText(i))
        self.tabs.clear()
        for name in opened_tabs:
            table = self.database.get_table(name)
            self.show_table(table)
        self.tabs.setCurrentIndex(current_opened_index)

    def delete_warning_dialog(self, info: str) -> bool:

        result = QMessageBox.question(self, "U sure?", info, QMessageBox.Ok | QMessageBox.Cancel, defaultButton= QMessageBox.Cancel )
        if result == QMessageBox.Ok:
            return True
        else:
            return False

    def delete_table(self):
        current_tab_name = self.tabs.tabText(self.tabs.currentIndex())
        should_delete = self.delete_warning_dialog(f"Do you really want to delete table \"{current_tab_name}\" ???")
        if should_delete:
            self.database.drop_table(current_tab_name)
            self.tabs.removeTab(self.tabs.currentIndex())
            self.update_table_list()
