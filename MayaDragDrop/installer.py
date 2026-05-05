# to reload we may need to do the following
# import sys
# sys.modules.pop("installer",None)


def onMayaDroppedPythonFile(*args, **kwargs):
    print("installer dropped")
    try:
        import os
        import sys

        import maya.cmds as cmds
        import maya.mel as mel

        PAYLOAD = '''
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


# If we have a dialog open already close
try:
    simple_dialog.close()
    simple_dialog.deleteLater()
except:
    pass

simple_dialog = SimpleDialog()
simple_dialog.show()
        '''

        SHELF_NAME = "MyTool"  # Internal shelf name (no spaces)
        SHELF_LABEL = "MyTool"  # Tab label shown in Maya UI

        BUTTON_LABEL = "My Button"  # Text shown beneath the button
        BUTTON_ICON = "commandButton.png"  # Maya built-in icon (or abs path to .png/.svg)
        BUTTON_ANNOTATION = "Run My Tool script"  # Tooltip

        def _get_main_shelves_layout():
            """Return the top-level shelf tab layout name used by Maya."""
            # Maya stores all shelves under the main shelf layout
            main_window = mel.eval("$tmpVar = $gShelfTopLevel")
            return main_window

        def _shelf_exists(shelf_name):
            """Return True if a shelf tab with shelf_name already exists."""
            shelves_layout = _get_main_shelves_layout()
            existing = cmds.tabLayout(shelves_layout, query=True, childArray=True) or []
            return shelf_name in existing

        def _find_button(shelf_name, button_label):
            """
            Return the full path of the shelfButton whose label matches button_label,
            or None if not found.
            """
            buttons = cmds.shelfLayout(shelf_name, query=True, childArray=True) or []
            for btn in buttons:
                if cmds.objectTypeUI(btn) == "shelfButton":
                    lbl = cmds.shelfButton(btn, query=True, label=True)
                    if lbl == button_label:
                        return btn
            return None

        # ─────────────────────────────────────────────
        # Main logic
        # ─────────────────────────────────────────────

        def setup_shelf():
            print("setting up shelf")
            shelves_layout = _get_main_shelves_layout()

            if _shelf_exists(SHELF_NAME):
                print(f"[MyTool] Shelf '{SHELF_NAME}' already exists.")
            else:
                # Create a new shelf tab
                cmds.setParent(shelves_layout)
                cmds.shelfLayout(SHELF_NAME, parent=shelves_layout)

                # Set the visible tab label (Maya uses the layout name as the tab key)
                cmds.tabLayout(shelves_layout, edit=True, tabLabel=(SHELF_NAME, SHELF_LABEL))

                print(f"[MyTool] Shelf '{SHELF_NAME}' created.")

            existing_btn = _find_button(SHELF_NAME, BUTTON_LABEL)

            if existing_btn:
                # Button exists then update its script only
                cmds.shelfButton(existing_btn, edit=True, command=PAYLOAD)
                print(f"[MyTool] Button '{BUTTON_LABEL}' found – script updated.")

            else:
                # Button does not exist create it
                cmds.setParent(SHELF_NAME)
                cmds.shelfButton(
                    label=BUTTON_LABEL,
                    annotation=BUTTON_ANNOTATION,
                    image1=BUTTON_ICON,
                    command=PAYLOAD,
                    sourceType="python",
                    parent=SHELF_NAME,
                )
                print(f"[MyTool] Button '{BUTTON_LABEL}' created on shelf '{SHELF_NAME}'.")
            """This function is called when the user drops this file into the Maya viewport."""

    except Exception:
        import traceback

        traceback.print_exc()
    setup_shelf()
