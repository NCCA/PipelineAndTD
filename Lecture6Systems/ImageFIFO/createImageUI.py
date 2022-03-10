#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PyQt5 import uic
    from PyQt5.QtCore import *
    from PyQt5.QtGui import  QSurfaceFormat
    from PyQt5.QtWidgets import QApplication,QMainWindow

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

sys.path.insert(0, "../ByteImage")
import ByteImage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        uic.loadUi("form.ui", self)  # Load the .ui file
        self.width.valueChanged.connect(self.transmit_size)
        self.height.valueChanged.connect(self.transmit_size)
        self.start_sim.pressed.connect(self.toggle_sim)
        self.timer = QTimer()
        self.timer.timeout.connect(self.transmit_data)

    def toggle_sim(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_sim.setText("Start")
        else:
            self.timer.start(self.timer_duration.value())
            self.start_sim.setText("Stop")

    def send_lines(self):
        rx = random.randint
        img = ByteImage.ByteImage(
            self.width.value(), self.height.value(), 255, 255, 255, 255
        )
        img.clear(255, 255, 255)
        cx = rx(1, img.width - 1)
        cy = rx(1, img.height - 1)
        for x in range(0, 1000):
            img.line(
                cx,
                cy,
                rx(1, img.width - 1),
                rx(1, img.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        with open(self.fifo_name.text(), "wb") as fifo:
            fifo.write(img.pixels)

    def send_check(self):
        rx = random.randint
        img = ByteImage.ByteImage(
            self.width.value(), self.height.value(), 255, 255, 255, 255
        )
        img.checker(
            rx(0, 255), rx(0, 255), rx(0, 255), rx(0, 255), rx(0, 255), rx(0, 255)
        )
        with open(self.fifo_name.text(), "wb") as fifo:
            fifo.write(img.pixels)

    def send_pixel(self):
        img = ByteImage.ByteImage(
            self.width.value(), self.height.value(), 255, 255, 255, 255
        )
        img.random_pixels()
        with open(self.fifo_name.text(), "wb") as fifo:
            fifo.write(img.pixels)

    def transmit_data(self):
        if self.mode.currentIndex() == 0:
            self.send_lines()
        elif self.mode.currentIndex() == 1:
            self.send_check()
        elif self.mode.currentIndex() == 2:
            self.send_pixel()

    def transmit_size(self):
        with open("imagefifo", "wb") as fifo:
            fifo.write(f"resize {self.width.value()} {self.height.value()}".encode())

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
