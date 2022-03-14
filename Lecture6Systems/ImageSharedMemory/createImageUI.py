#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import *
    from PyQt5.QtGui import QSurfaceFormat
    from PyQt5.QtWidgets import QApplication, QMainWindow

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6 import uic
    from PyQt6.QtCore import QEvent, Qt, QTimer
    from PyQt6.QtGui import QSurfaceFormat
    from PyQt6.QtWidgets import QApplication, QMainWindow

    PyQtVersion = 6

import math
import random
import sys
from multiprocessing import shared_memory

sys.path.insert(0, "../ByteImage")
import ByteImage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        uic.loadUi("form.ui", self)  # Load the .ui file
        self.start_sim.pressed.connect(self.toggle_sim)
        self.timer = QTimer()
        self.timer.timeout.connect(self.transmit_data)
        self.shm = shared_memory.SharedMemory(name="imageMap")
        self.width = 400
        self.height = 400
        self.img = ByteImage.ByteImage(self.width, self.height, 255, 255, 255, 255)

    def closeEvent(self, event):
        self.timer.stop()
        self.shm.close()

    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_sim.setText("Start")
        else:
            self.timer.start(self.timer_duration.value())
            self.start_sim.setText("Stop")

    def update_memory(self):
        # should be a better way of doing this
        for i in range(0, len(self.img.pixels)):
            self.shm.buf[i] = self.img.pixels[i]

    def send_lines(self):
        rx = random.randint
        self.img.clear(255, 255, 255)
        cx = rx(1, self.img.width - 1)
        cy = rx(1, self.img.height - 1)
        for x in range(0, 1000):
            self.img.line(
                cx,
                cy,
                rx(1, self.img.width - 1),
                rx(1, self.img.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        self.update_memory()

    def send_check(self):
        rx = random.randint
        self.img.checker(
            rx(0, 255), rx(0, 255), rx(0, 255), 255, 255, 255, check_size=rx(5, 50)
        )
        self.update_memory()

    def send_pixel(self):
        self.img = ByteImage.ByteImage(self.width, self.height, 255, 255, 255, 255)
        self.img.random_pixels()
        self.update_memory()

    def transmit_data(self):
        if self.mode.currentIndex() == 0:
            self.send_lines()
        elif self.mode.currentIndex() == 1:
            self.send_check()
        elif self.mode.currentIndex() == 2:
            self.send_pixel()

    if PyQtVersion == 5:

        def keyPressEvent(self, event):
            key = event.key()
            if key == Qt.Key_Escape:
                exit()
            self.update()

    else:  # Qt6 Versions

        def keyPressEvent(self, event):
            key = event.key()
            if key == Qt.Key.Key_Escape:
                exit()
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(200, 200)
    window.show()
    if PyQtVersion == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())
