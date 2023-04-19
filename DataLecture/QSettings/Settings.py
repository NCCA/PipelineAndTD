#!/usr/bin/env python
try:  #  support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import *
    from PyQt5.QtGui import QCloseEvent, QColor, QPalette
    from PyQt5.QtWidgets import (QApplication, QColorDialog, QMainWindow,
                                 QPushButton, QVBoxLayout)

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6 import uic
    from PyQt6.QtCore import *
    from PyQt6.QtGui import QCloseEvent, QColor, QPalette
    from PyQt6.QtWidgets import (QApplication, QColorDialog, QMainWindow,
                                 QPushButton, QVBoxLayout)
    PyQtVersion = 6

import sys


class MainWindow(QMainWindow):
    """Main Window Class"""
    def __init__(self):
        """Initialize the Main Window"""
        super(MainWindow, self).__init__()
        self.settings = QSettings("NCCA", "NCCA_Settings_Demo")
        # add button to select colour
        self.button = QPushButton("Select Colour")
        self.setCentralWidget(self.button)
        self.button.clicked.connect(self.select_colour)
        self.load_settings()

    def load_settings(self) :
        """Load the settings"""
        self.resize(self.settings.value("size", QSize(100, 100)))
        # load the background colour
        colour=self.settings.value("background_colour", QColor(255,255,255))
        self.setStyleSheet(f"background-color: {colour.name()}")

    def save_settings(self)   :
        """Save the settings"""
        self.settings.setValue("size", self.size())  
        # save the background colour
        self.settings.setValue("background_colour", self.palette().color(QPalette.ColorRole.Window))

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle the close event"""
        self.save_settings()

    def select_colour(self):
        """Select the colour"""
        colour = QColorDialog.getColor()
        if colour.isValid():
            self.setStyleSheet(f"background-color: {colour.name()};")




if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
