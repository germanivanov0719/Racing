# Main libs imports
import pygame
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QCloseEvent
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
from gameplay.settings_menu.settings import settings

# System constants
from main import VERSION

# Game constants
from resources.fonts.FONTS import ORBITRON_REGULAR, ORBITRON_MEDIUM, ORBITRON_EXTRA_BOLD


class SettingsMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/Settings/settings.ui', self)
        self.setWindowTitle('Settings')

        # Setting previous values
        self.framerate_spin.setValue(settings.FPS)
        self.gsf_spin.setValue(float(settings.GSF))
        self.precise_framerate_box.setChecked(settings.PRECISE_FPS)
        self.vsync_box.setChecked(settings.VSYNC)

        # Connecting
        self.save_btn.pressed.connect(self.save)


    def save(self):
        settings.FPS = self.framerate_spin.value()
        settings.GSF = self.gsf_spin.value()
        settings.PRECISE_FPS = bool(self.precise_framerate_box.checkState())
        settings.VSYNC = bool(self.vsync_box.checkState())
        if self.controls.checkedButton() == self.wasd_btn:
            settings.CONTROLS = 'WASD'
        else:
            settings.CONTROLS = 'Arrows'
        self.close()



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


if __name__ == '__main__':
    main()
