# Main libs imports
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

# Other libs imports
import sys

# Other game parts
# EMPTY

# System constants
from main import VERSION

# Game constants
# EMPTY


def generate_welcome():
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setWindowTitle('Welcome!')
    w.setText(f'New: \n\n'
              f'- Optimization and code cleanup.\n'
              f'- Stability improvements.\n'
              f'This version has no known issues.\n'
              f'If you find some, contact the development team.\n\n'
              f'See more detailed changelog on GitHub.'
              f'\n\nVersion: {VERSION}\t\t\t')
    w.exec()
