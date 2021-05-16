"""
main file
start wx framework and launch GUI
"""
import logging
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from src.gui.main_frame import MainFrame

logging.basicConfig(format='%(levelname)s :: %(message)s', level=logging.DEBUG)

logging.info('Program starting')

app = QApplication(sys.argv)
ex = MainFrame()
ex.show()
logging.info('Program started')
sys.exit(app.exec_())

