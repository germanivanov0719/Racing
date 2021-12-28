# Main libs imports
import pygame
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

# Other libs imports
import sys
import random

# Other game parts
import gameplay.start_menu.start_menu
import gameplay.car_menu.car_menu
import resources.Highways.Highway
import gameplay.race.race
import gameplay

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class SettingsMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/Settings/settings.ui', self)
        self.setWindowTitle('Settings')
        # Your code

    # def closeEvent(self, event) -> None:
    #     self.hide()
    #     event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    # Fix HiDPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    ex = SettingsMenu()
    ex.show()
    sys.excepthook = except_hook
    app.exec_()
    del app
    del ex
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
