import logging

from PyQt5.QtWidgets import QListWidget


class MainFrame(QListWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self) :
        self.resize(300, 120)

        self.addItem("Item 1")
        self.addItem("Item 2")
        self.addItem("Item 3")
        self.addItem("Item 4")

        self.setWindowTitle('Test')


