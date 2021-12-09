import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

from main import VERSION

def generate_welcome():
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setWindowTitle('Welcome!')
    w.setText(f'Welcome! In the current state the program isn\'t doing anything '
              f'useful. You can explore the internal files to understand how the code is supposed to work in the future'
              f'\n\nVersion: {VERSION}\t\t\t')
    w.exec()