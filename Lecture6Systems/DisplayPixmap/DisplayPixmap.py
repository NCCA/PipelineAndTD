#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PyQt5.QtCore import *
    from PyQt5.QtGui import QMainWindow
    from PyQt5.QtWidgets import QApplication

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QImage, QPixmap
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

    PyQtVersion = 6

import argparse
import random
import sys

sys.path.insert(0, "../ByteImage")
import ByteImage


class MainWindow(QMainWindow):
    def __init__(self, width: int = 800, height: int = 800, mode="lines"):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)
        self.width = int(width)
        self.height = int(height)
        self.image = ByteImage.ByteImage(self.width, self.height, 128, 128, 128, 255)
        self.label = QLabel(self)
        self.update_image()
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.timer = QTimer()
        if mode == "lines":
            self.timer.timeout.connect(self.random_lines)
        else:
            self.timer.timeout.connect(self.random_pixels)

        self.timer.start(0)

    def random_pixels(self):
        self.image.random_pixels()
        self.update_image()

    def random_lines(self):
        self.image.clear(255, 255, 255)
        rx = random.randint
        cx = rx(1, self.width - 1)
        cy = rx(1, self.height - 1)
        for i in range(0, 200):
            self.image.line(
                cx,
                cy,
                rx(1, self.width - 1),
                rx(1, self.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        self.update_image()

    def update_image(self):
        img = QImage(
            self.image.pixels,
            self.width,
            self.height,
            QImage.Format.Format_RGBA8888
            if PyQtVersion == 6
            else QImage.Format_RGBA8888,
            None,
        )

        self.pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(self.pixmap)

    if PyQtVersion == 5:

        def keyPressEvent(self, event):
            key = event.key()
            if key == Qt.Key_Escape:
                exit()

    else:  # Qt6 Versions

        def keyPressEvent(self, event):
            key = event.key()
            if key == Qt.Key.Key_Escape:
                exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple ImageBuffer Viewer")

    parser.add_argument(
        "--width",
        "-w",
        nargs="?",
        const=400,
        default=400,
        type=int,
        help="width of image default 400",
    )
    parser.add_argument(
        "--height",
        "-ht",
        nargs="?",
        const=400,
        default=400,
        type=int,
        help="height of image default 400",
    )
    parser.add_argument(
        "--pixels", "-p", action="count", help="draw pixels instead of lines"
    )
    mode = "lines"
    args = parser.parse_args()
    if args.pixels:
        mode = "points"
    app = QApplication(sys.argv)
    w = MainWindow(args.width, args.height, mode)
    w.show()
    if PyQtVersion == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())
