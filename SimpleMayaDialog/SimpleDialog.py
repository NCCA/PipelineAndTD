import sys

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtCore, QtWidgets
from shiboken6 import wrapInstance


def get_main_window():
    """this returns the maya main window for parenting"""
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QDialog)


class SimpleDialog(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window()):
        super().__init__(parent)
        self.setWindowTitle("Simple Dialog")
        self.resize(200, 180)
        self.gridLayout = QtWidgets.QGridLayout(self)


if __name__ == "__main__":
    # If we have a dialog open already close
    try:
        simple_dialog.close()
        simple_dialog.deleteLater()
    except:
        pass

    simple_dialog = SimpleDialog()
    simple_dialog.show()
