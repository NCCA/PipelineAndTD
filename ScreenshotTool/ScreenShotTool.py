import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance


def get_main_window():
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QDialog)


class ScreenShotsDialog(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window()):
        if sys.version_info.major == 3:
            super().__init__(parent)
        # python 2
        else:
            super(ScreenShotsDialog, self).__init__(self)
        self.setWindowTitle("Screen shot Tool")

        self.resize(190, 148)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.screenshot = QtWidgets.QPushButton("Screen Shot", self)
        self.screenshot.pressed.connect(self.save_screenshots)
        self.screenshot.setObjectName("screenshot")
        self.gridLayout.addWidget(self.screenshot, 3, 1, 1, 1)
        self.base_name = QtWidgets.QLineEdit("base_name", self)
        self.base_name.setObjectName("base_name")
        self.gridLayout.addWidget(self.base_name, 0, 0, 1, 2)
        self.width = QtWidgets.QSpinBox(self)
        self.width.setMinimum(64)
        self.width.setMaximum(1024)
        self.width.setProperty("value", 128)
        self.width.setObjectName("width")
        self.gridLayout.addWidget(self.width, 2, 0, 1, 1)
        self.height = QtWidgets.QSpinBox(self)
        self.height.setMinimum(64)
        self.height.setMaximum(1024)
        self.height.setSingleStep(0)
        self.height.setProperty("value", 128)
        self.height.setObjectName("height")
        self.gridLayout.addWidget(self.height, 2, 1, 1, 1)
        self.Cancel = QtWidgets.QPushButton("Cancel", self)
        self.Cancel.setObjectName("Cancel")
        self.Cancel.clicked.connect(self.close)
        self.gridLayout.addWidget(self.Cancel, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel("Width", self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel("Height", self)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

    def save_screenshots(self):
        path = cmds.fileDialog2(fm=3)

        views = [
            "cmds.viewSet(p=True, fit=True)",
            "cmds.viewSet(t=True, fit=True)",
            "cmds.viewSet(s=True, fit=True)",
            "cmds.viewSet(f=True, fit=True)",
        ]
        for i in range(0, 4):
            eval(views[i])
            view = OpenMayaUI.M3dView.active3dView()
            panel = cmds.getPanel(visiblePanels=True)
            cmds.setFocus(panel[0])
            pm.viewFit()
            image = OpenMaya.MImage()
            view.refresh()
            view.readColorBuffer(image, True)
            image.resize(
                self.width.value(), self.height.value(), preserveAspectRatio=True
            )
            name = ["Persp", "Top", "Side", "Front"]
            image.writeToFile(
                "{}/{}{}.png".format(path[0], self.base_name.text(), name[i]),
                outputFormat="png",
            )


if __name__ == "__main__":

    w = ScreenShotsDialog()
    w.show()
