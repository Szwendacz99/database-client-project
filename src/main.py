"""
main file
start wx framework and launch GUI
"""

import settings
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from src.gui.main_frame import MainFrame

app = QApplication(sys.argv)
ex = MainFrame()
ex.show()
settings.info('Program started')
sys.exit(app.exec_())

