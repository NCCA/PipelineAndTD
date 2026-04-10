#!/usr/bin/env python
import os
import platform
import sys
from pathlib import Path

maya_locations = {
    "Linux": "/maya",
    "Darwin": "/Library/Preferences/Autodesk/maya",
    "Windows": "\\Documents\\maya\\version",
}

MODULE_NAME = "MayaPluginDemos"


def install_module(location):
    print(f"installing to {location}")
    # first write the module file
    current_dir = Path.cwd()
    if not Path(location + f"modules/{MODULE_NAME}.mod").is_file():
        print("writing module file")
        with open(location + f"modules/{MODULE_NAME}.mod", "w") as file:
            file.write(f"+ {MODULE_NAME} 1.0 {current_dir}\n")
            # in this case we are putting modules in the root but in bigger systems we
            # would use plug-ins
            # file.write("MAYA_PLUG_IN_PATH +:= plug-ins\n")


def check_maya_installed(op_sys):
    mloc = f"{Path.home()}{maya_locations.get(op_sys)}/"
    if not os.path.isdir(mloc):
        raise
    return mloc


if __name__ == "__main__":
    op_sys = platform.system()
    try:
        m_loc = check_maya_installed(op_sys)
    except:
        print("Error can't find maya install")
        sys.exit(os.EX_CONFIG)

    install_module(m_loc)
