#!/usr/bin/env python
try:  #  support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import *
    from PyQt5.QtGui import QCloseEvent
    from PyQt5.QtWidgets import QApplication, QMainWindow

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6 import uic
    from PyQt6.QtCore import *
    from PyQt6.QtGui import QCloseEvent
    from PyQt6.QtWidgets import QApplication, QMainWindow
    PyQtVersion = 6

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.settings = QSettings("NCCA", "NCCA_Settings_Demo")
        self.load_settings()

    def load_settings(self) :
        self.resize(self.settings.value("size", QSize(100, 100)))

    def save_settings(self)   :
        self.settings.setValue("size", self.size())  

    def closeEvent(self, event: QCloseEvent) -> None:
        self.save_settings()




if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
