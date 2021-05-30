import logging
from PyQt5.QtWidgets import QListWidget, QMainWindow, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QPushButton, \
    QDockWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


log = logging.getLogger(__name__)


class MainFrame(QMainWindow):

    def __init__(self):
        """
        Main Window class
        """
        super().__init__()

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
        layout_buttons.addWidget(QPushButton("button 1"), alignment=Qt.AlignLeft)
        layout_buttons.addWidget(QPushButton("button 2"), alignment=Qt.AlignLeft)
        layout_buttons.addWidget(QPushButton("button 3"), alignment=Qt.AlignLeft)
        layout_buttons.addWidget(QPushButton("button 4"), alignment=Qt.AlignLeft)

        box.setLayout(layout_buttons)
        layout.addWidget(box, 0, 0, 4, 10)

        self.tabs = QTabWidget(self.central_widget)

        tabletest = QTableWidget()
        tabletest.setRowCount(3)
        tabletest.setColumnCount(3)
        # header = QHeaderView(Qt.Horizontal, tabletest)
        # header.tex
        tabletest.setHorizontalHeaderItem(0, QTableWidgetItem("column 1"))
        tabletest.setHorizontalHeaderItem(1, QTableWidgetItem("column 2"))
        tabletest.setHorizontalHeaderItem(2, QTableWidgetItem("column 3"))

        for i in range(3):
            for j in range(3):
                tabletest.setItem(i, j, QTableWidgetItem(f"item {i}:{j}"))
        self.tabs.addTab(tabletest, "Table test")

        layout.addWidget(self.tabs, 4, 0, 100, 10)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def create_docking_tables_list_panel(self):
        """
        Create docking widget with list of tables
        :return: None
        """
        self.table_list_dockable = QDockWidget("Tables", self)
        self.table_list = QListWidget(self.central_widget)
        self.table_list_dockable.setWidget(self.table_list)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.table_list_dockable)



