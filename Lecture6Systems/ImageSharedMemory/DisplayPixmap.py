#!/usr/bin/env python
try:  # support either PyQt5 or 6
    from PyQt5.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal
    from PyQt5.QtGui import QImage, QPixmap
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

    PyQtVersion = 5
except ImportError:
    print("trying Qt6")
    from PyQt6.QtCore import *
    from PyQt6.QtGui import QImage, QPixmap
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

    PyQtVersion = 6
import argparse
import errno
import os
import random
import sys
import time
from multiprocessing import shared_memory


class MainWindow(QMainWindow):
    def __init__(self, width: int = 800, height: int = 800):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)
        self.width = int(width)
        self.height = int(height)
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.resize(self.width, self.height)
        self.shm = shared_memory.SharedMemory(
            create=True, size=(self.width * self.height * 4), name="imageMap"
        )
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1)

    def closeEvent(self, event):
        self.shm.close()
        self.shm.unlink()

    def update_image(self):
        img = QImage(
            self.shm.buf,
            self.width,
            self.height,
            QImage.Format.Format_RGBA8888
            if PyQtVersion == 6
            else QImage.Format_RGBA8888,
        )
        self.pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(self.pixmap)
        self.update()

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

    args = parser.parse_args()

    app = QApplication(sys.argv)
    w = MainWindow(args.width, args.height)
    w.show()
    if PyQtVersion == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())
