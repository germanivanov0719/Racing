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
              f'- Still implementing the Game Engine.\n'
              f'See detailed changelog on GitHub.'
              f'\n\nVersion: {VERSION}\t\t\t')
    w.exec()
