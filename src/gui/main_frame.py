import PyQt5.QtCore
from PyQt5.QtWidgets import QListWidget, QMainWindow, QTabWidget, QGridLayout, QGroupBox, QHBoxLayout, QPushButton
import src.settings as settings
from PyQt5.QtCore import Qt


class MainFrame(QMainWindow):

    def __init__(self):
        """
        Main Window class
        """
        super().__init__()
        self.central_widget = None
        self.tabs = None
        self.table_list = None
        self.setup_ui()

    def setup_ui(self):
        """
        Create main window
        :return: None
        """
        settings.debug("Setting up GUI....")
        self.resize(300, 120)

        self.create_central_widget()

        self.setWindowTitle('Test')

    def create_central_widget(self):
        """
        create central widget with tables chosing widget on the left
        and QTabWidget for main display in the center/right
        :return: None
        """
        settings.debug("Creating central widget....")
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
        layout.addWidget(box, 0, 1, 1, 3)

        self.table_list = QListWidget(self.central_widget)
        self.table_list.addItem("tab1")
        self.table_list.addItem("tab2")
        self.table_list.addItem("tab3")
        self.table_list.addItem("tab4")
        layout.addWidget(self.table_list, 0, 0, 10, 1, alignment=Qt.AlignLeft)

        self.tabs = QTabWidget(self.central_widget)

        layout.addWidget(self.tabs, 1, 1, 9, 3)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)





