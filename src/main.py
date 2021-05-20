"""
main file
start wx framework and launch GUI
"""

import settings
import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_frame import MainFrame

app = QApplication(sys.argv)
frame = MainFrame()
settings.info('Program started')

sys.exit(app.exec_())

