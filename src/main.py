"""
main file
start wx framework and launch GUI
"""
import logging

import settings
import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_frame import MainFrame

logging.basicConfig(format='%(levelname)s |%(name)s| %(message)s', level=logging.DEBUG)

log = logging.getLogger(__name__)

app = QApplication(sys.argv)
frame = MainFrame()
log.info('Program started')

sys.exit(app.exec_())

