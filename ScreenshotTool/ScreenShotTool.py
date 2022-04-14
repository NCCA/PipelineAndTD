import sys

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance


def get_main_window():
    """this returns the maya main window for parenting"""
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QDialog)


class ScreenShotsDialog(QtWidgets.QDialog):
    def __init__(self, parent=get_main_window()):
        """init the class and setup dialog"""
        # Python 3 does inheritance differently to 2 so support both
        # as Maya 2020 is still Python 2
        if sys.version_info.major == 3:
            super().__init__(parent)
        # python 2
        else:
            super(ScreenShotsDialog, self).__init__(parent)
        # Set the GUI components and layout
        self.setWindowTitle("Screenshot Tool")
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
        """This does all the work"""
        # Get the folder to save to
        path = cmds.fileDialog2(fm=3)
        # We evaluate these commands to set the view
        # for the screen shot
        views = [
            "cmds.viewSet(p=True, fit=True)",
            "cmds.viewSet(t=True, fit=True)",
            "cmds.viewSet(s=True, fit=True)",
            "cmds.viewSet(f=True, fit=True)",
        ]
        # This is used to see if the view should be exported
        isActive = [
            "self.persp.isChecked()",
            "self.top.isChecked()",
            "self.side.isChecked()",
            "self.front.isChecked()",
        ]
        # loop for each view
        for i in range(0, 4):
            # is if it should be exported
            if eval(isActive[i]):
                # Set the active view
                eval(views[i])
                # grab the view from maya
                view = OpenMayaUI.M3dView.active3dView()
                # need to set focus for the frame command
                panel = cmds.getPanel(visiblePanels=True)
                cmds.setFocus(panel[0])

                if self.frame_all.isChecked():
                    pm.viewFit()
                # now dump to MImage
                image = OpenMaya.MImage()
                view.refresh()
                show_manip = self.view_manip.isChecked()
                cmds.viewManip(v=show_manip)
                view.readColorBuffer(image, True)
                # resize to selected size
                image.resize(
                    self.width.value(), self.height.value(), preserveAspectRatio=True
                )
                name = ["Persp", "Top", "Side", "Front"]
                # write
                image.writeToFile(
                    "{}/{}{}.png".format(path[0], self.base_name.text(), name[i]),
                    outputFormat="png",
                )
        self.close()


if __name__ == "__main__":

    # If we have a dialog open already close
    try:
        screen_shot_dialog.close()
        screen_shot_dialog.deleteLater()
    except:
        pass

    screen_shot_dialog = ScreenShotsDialog()
    screen_shot_dialog.show()
