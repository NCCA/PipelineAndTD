# Houdini Package Demo

This demo demonstrates a simple method to generate and install a [houdini package](https://www.sidefx.com/docs/houdini/ref/plugins.html) and install it in the users current houdini setup.

This project consists of two parts, the [installHouPackage.py](installHouPackage.py) file which contains the code to generate the package and install it, and the [scripts](scripts) folder which contains the actual package code.

In this example the installHoudiniPackage.py file will generate a package called "TestUI" which sets up the PYTHONPATH to point to the install directory of the package / scripts as well as setting a custom environment variable called CUSTOM_ENV.

## installHouPackage.py

At present this script has been tested on Linux and Mac but can be modified for Windows, set the houdini_version and the script will auto detect the os.

```python
houdini_version = "20.5"

houdini_locations = {
    "Linux": f"/houdini{houdini_version}/",
    "Darwin": f"/Library/Preferences/houdini/{houdini_version}",
    #    "Windows": "\\Documents\\houdini\\", don't have a windows machine to test
}
```

The core installation in this demo sets only two core package elements "load_package_one" and the env array which contains dictionary elements with the key and value pairs for the environment variables.


```json
{
  "load_package_once": "true",
  "env": [
    {
      "CUSTOM_ENV": "/Volumes/teaching/Code/PipelineAndTD/HoudiniPackage"
    },
    {
      "PYTHONPATH": "/Volumes/teaching/Code/PipelineAndTD/HoudiniPackage/scripts"
    }
  ]
}
```

One startup this package will be loaded and in the case of this demo we will see that the PYTHONPATH has been appended with the path to the scripts folder and the CUSTOM_ENV variable has been set to the install directory of the package.

We can query the CUSTOM_ENV variable in the python shell to see if it has been set correctly.

```python
import hou
hou.getenv("CUSTOM_ENV")
```

Now that the PYTHONPATH has been updated we can add a custom tool to our shelf and add the following python code to the shelf tool.

```python
import sys
if "CustomDialog" in sys.modules :
    del sys.modules["CustomDialog"]
from CustomDialog import run_package

run_package()
```


This will import the CustomDialog module from the package and run the run_package function which will open a simple dialog displaying the environment variable CUSTOM_ENV.

Note the del function is used to demonstrate the unloading of the module so you can make changes to the source code and re-load / run the script.


# CustomDialog.py

This script is using the build in PySide2 for Houdini 20.5 in the future this will be updated to use PySide6. In some cases I use [qtpy](https://pypi.org/project/QtPy/) to ensure future compatibility with PySide6.

To install this you can use the following command in the houdini shell

```bash
hython -m pip install qtpy
```

The overall script is simple

```python
import hou
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(hou.getenv("CUSTOM_ENV"))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel(hou.getenv("CUSTOM_ENV")))
        self.resize(800, 100)


def run_package():
    # Parent to Houdini main window
    dialog = MyDialog(parent=hou.ui.mainQtWindow())
    dialog.show()  # or dialog.exec() for modal
```

The core thing to remember with Qt is that it needs a correct parent when constructing the dialog. In this case we are using the main window of Houdini as the parent. This will ensure that the dialog is displayed correctly in Houdini and is not a separate window.

If you want to use the dialog as a modal dialog you can use the exec() function instead of show(). This will block the main window until the dialog is closed. In this case we are using show() to display the dialog and allow the user to interact with it.