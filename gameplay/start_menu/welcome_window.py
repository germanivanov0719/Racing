# Main libs imports
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox

# Other libs imports
import sys

# Other game parts
# import gameplay.car_menu.car_menu

# System constants
from main import VERSION

# Game constants
# EMPTY


def generate_welcome():
    app = QApplication(sys.argv)
    w = QMessageBox()
    w.setWindowTitle('Welcome!')
    w.setText(f'New: \n'
              f'1.9 screens are already implemented. \n'
              f'Added test vehicles, added vehicle scroll, other improvements.\n'
              f'\n\nVersion: {VERSION}\t\t\t')
    w.exec()