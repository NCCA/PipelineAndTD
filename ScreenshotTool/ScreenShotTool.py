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
            super(ScreenShotsDialog, self).__init__(parent)
        self.setWindowTitle("Screen shot Tool")

        self.resize(200, 180)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.screenshot = QtWidgets.QPushButton("Screen Shot", self)
        self.screenshot.pressed.connect(self.save_screenshots)
        self.gridLayout.addWidget(self.screenshot, 4, 1, 1, 1)
        self.base_name = QtWidgets.QLineEdit("base_name", self)
        self.gridLayout.addWidget(self.base_name, 0, 0, 1, 2)
        self.width = QtWidgets.QSpinBox(self)
        self.width.setMinimum(64)
        self.width.setMaximum(1024)
        self.width.setProperty("value", 128)
        self.gridLayout.addWidget(self.width, 3, 0, 1, 1)
        self.height = QtWidgets.QSpinBox(self)
        self.height.setMinimum(64)
        self.height.setMaximum(1024)
        self.height.setSingleStep(0)
        self.height.setProperty("value", 128)
        self.gridLayout.addWidget(self.height, 3, 1, 1, 1)
        self.Cancel = QtWidgets.QPushButton("Cancel", self)
        self.Cancel.clicked.connect(self.close)
        self.gridLayout.addWidget(self.Cancel, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel("Width", self)
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel("Height", self)
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.top = QtWidgets.QCheckBox("Top", self.groupBox)
        self.top.setChecked(True)
        self.gridLayout_2.addWidget(self.top, 0, 0, 1, 1)
        self.persp = QtWidgets.QCheckBox("Persp", self.groupBox)
        self.persp.setChecked(True)
        self.gridLayout_2.addWidget(self.persp, 0, 1, 1, 1)
        self.side = QtWidgets.QCheckBox("Side", self.groupBox)
        self.side.setChecked(True)
        self.gridLayout_2.addWidget(self.side, 1, 0, 1, 1)
        self.front = QtWidgets.QCheckBox("Front", self.groupBox)
        self.front.setChecked(True)
        self.gridLayout_2.addWidget(self.front, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)
        self.frame_all = QtWidgets.QCheckBox("Frame All", self)
        self.frame_all.setChecked(True)
        self.gridLayout.addWidget(self.frame_all, 2, 0, 1, 1)
        self.view_manip = QtWidgets.QCheckBox("Show View Cube", self)
        self.view_manip.setChecked(True)
        self.gridLayout.addWidget(self.view_manip, 2, 1, 1, 1)

    def save_screenshots(self):
        path = cmds.fileDialog2(fm=3)

        views = [
            "cmds.viewSet(p=True, fit=True)",
            "cmds.viewSet(t=True, fit=True)",
            "cmds.viewSet(s=True, fit=True)",
            "cmds.viewSet(f=True, fit=True)",
        ]
        isActive = [
            "self.persp.isChecked()",
            "self.top.isChecked()",
            "self.side.isChecked()",
            "self.front.isChecked()",
        ]
        for i in range(0, 4):
            if eval(isActive[i]):
                eval(views[i])
                show_manip = self.view_manip.isChecked()

                view = OpenMayaUI.M3dView.active3dView()
                panel = cmds.getPanel(visiblePanels=True)
                cmds.setFocus(panel[0])
                if self.frame_all.isChecked():
                    pm.viewFit()
                image = OpenMaya.MImage()
                view.refresh()
                cmds.viewManip(v=show_manip)
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
