import sys

import hou
from PySide2 import QtCore, QtWidgets


class ScreenShotsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the GUI components and layout
        self.setWindowTitle("Screenshot Tool")
        self.resize(200, 180)
        # Main layout for form
        self.gridLayout = QtWidgets.QGridLayout(self)
        # LineEdit for the name to save screen shots
        # row 0
        self.base_name = QtWidgets.QLineEdit("base_name", self)
        self.gridLayout.addWidget(self.base_name, 0, 0, 1, 2)

        # row 1 Grid Box
        self.groupBox = QtWidgets.QGroupBox(self)
        self.gbGridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gbGridLayout.setObjectName("gbGridLayout")
        self.top = QtWidgets.QCheckBox("Top", self.groupBox)
        self.top.setChecked(True)
        self.gbGridLayout.addWidget(self.top, 0, 0, 1, 1)
        self.persp = QtWidgets.QCheckBox("Persp", self.groupBox)
        self.persp.setChecked(True)
        self.gbGridLayout.addWidget(self.persp, 0, 1, 1, 1)
        
        self.left = QtWidgets.QCheckBox("Left", self.groupBox)
        self.left.setChecked(True)
        self.gbGridLayout.addWidget(self.left, 1, 0, 1, 1)
        self.front = QtWidgets.QCheckBox("Front", self.groupBox)
        self.front.setChecked(True)
        self.gbGridLayout.addWidget(self.front, 1, 1, 1, 1)

        self.back = QtWidgets.QCheckBox("Back", self.groupBox)
        self.back.setChecked(True)
        self.gbGridLayout.addWidget(self.back, 2, 0, 1, 1)
        self.right = QtWidgets.QCheckBox("Right", self.groupBox)
        self.right.setChecked(True)
        self.gbGridLayout.addWidget(self.right, 2, 1, 1, 1)

        self.bottom = QtWidgets.QCheckBox("Bottom", self.groupBox)
        self.bottom.setChecked(True)
        self.gbGridLayout.addWidget(self.bottom, 3, 0, 1, 1)
        self.uv = QtWidgets.QCheckBox("UV", self.groupBox)
        self.uv.setChecked(True)
        self.gbGridLayout.addWidget(self.uv, 3, 1, 1, 1)


        # Add to main dialog
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        # frame all row 2
        self.frame_all = QtWidgets.QCheckBox("Frame All", self)
        self.frame_all.setChecked(True)
        self.gridLayout.addWidget(self.frame_all, 2, 0, 1, 1)



        # width and height row 3 Label row 4 spin control
        width_label = QtWidgets.QLabel("Width", self)
        self.gridLayout.addWidget(width_label, 3, 0, 1, 1)

        self.width = QtWidgets.QSpinBox(self)
        self.width.setMinimum(64)
        self.width.setMaximum(1024)
        self.width.setProperty("value", 128)
        self.gridLayout.addWidget(self.width, 4, 0, 1, 1)

        height_label = QtWidgets.QLabel("Height", self)
        self.gridLayout.addWidget(height_label, 3, 1, 1, 1)

        self.height = QtWidgets.QSpinBox(self)
        self.height.setMinimum(64)
        self.height.setMaximum(1024)
        self.height.setSingleStep(0)
        self.height.setProperty("value", 128)
        self.gridLayout.addWidget(self.height, 4, 1, 1, 1)
        
        # row 5
        # cancel button

        self.Cancel = QtWidgets.QPushButton("Cancel", self)
        self.Cancel.clicked.connect(self.close)
        self.gridLayout.addWidget(self.Cancel, 5, 0, 1, 1)

        # Screen Shot button

        self.screenshot = QtWidgets.QPushButton("Screen Shot", self)
        self.screenshot.pressed.connect(self.save_screenshots)
        self.gridLayout.addWidget(self.screenshot, 5, 1, 1, 1)


    def save_screenshots(self):
        """This does all the work"""
        # Get the folder to save to
        directory=hou.ui.selectFile(None,"Choose destination folder",False,hou.fileType.Directory,"","",False,False,hou.fileChooserMode.Write)
        if directory == "" :
            return
        # We evaluate these commands to set the view
        # for the screen shot
        # This is used to see if the view should be exported
        isActive = [
            "self.persp.isChecked()",
            "self.top.isChecked()",
            "self.left.isChecked()",
            "self.front.isChecked()",
            "self.back.isChecked()",
            "self.right.isChecked()",
            "self.bottom.isChecked()",
            "self.uv.isChecked()"            
        ]

        views=[hou.geometryViewportType.Perspective,
                hou.geometryViewportType.Top,
                hou.geometryViewportType.Left,
                hou.geometryViewportType.Front,
                hou.geometryViewportType.Back,
                hou.geometryViewportType.Right,
                hou.geometryViewportType.Bottom,
                hou.geometryViewportType.UV]

        name = ["Persp", "Top", "Left", "Front","Back","Right","Bottom","UV"]


        # Move to Build mode
        desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
        desktops_dict["Build"].setAsCurrent()
        scene_view=hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        viewport = scene_view.curViewport()
        frame=hou.frame()

        for i in range(0,len(name)) :
            if eval(isActive[i]) :
                filename=f"{directory}/{self.base_name.text()}{name[i]}.png" 
                viewport.changeType(views[i])
                if self.frame_all.isChecked():
                    viewport.frameAll()
                fbs = scene_view.flipbookSettings().stash()
                fbs.resolution((self.width.value(),self.height.value()))
                fbs.frameRange( (frame, frame) )
                fbs.output(filename)
                fbs.outputToMPlay(False)
                scene_view.flipbook(viewport, fbs)


dialog = ScreenShotsDialog()
dialog.show()

