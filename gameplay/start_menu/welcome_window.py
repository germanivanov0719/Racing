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
    w.setText(f'New: \n\n'
              f'- Window with earnings when game ends.\n'
              f'- You can now buy cars.\n'
              f'- Driving outside the highway is no longer possible.\n'
              f'- Stability improvements.\n'
              f'- A lot more other changes.\n'
              f'\nThis should be considered a stable release\n\n'
              f'See more detailed changelog on GitHub.'
              f'\n\nVersion: {VERSION}\t\t\t')
    w.exec()
