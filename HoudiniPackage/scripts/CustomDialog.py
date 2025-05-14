import hou
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(hou.getenv("CUSTOM_ENV"))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Hello from Qt!"))


def run_package():
    # Parent to Houdini main window
    dialog = MyDialog(parent=hou.ui.mainQtWindow())
    dialog.show()  # or dialog.exec() for modal
