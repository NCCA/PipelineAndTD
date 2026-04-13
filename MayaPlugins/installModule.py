#!/usr/bin/env python
"""
Maya Plugin Module Installer

This script installs a Maya plugin module by creating a .mod file
in the appropriate Maya preferences directory based on the operating system.
"""

import os
import platform
import sys
from pathlib import Path

maya_locations: dict[str, str] = {
    "Linux": "/maya",
    "Darwin": "/Library/Preferences/Autodesk/maya",
    "Windows": "\\Documents\\maya\\version",
}

MODULE_NAME: str = "MayaPluginDemos"


def install_module(location: str) -> None:
    """
    Install the Maya module by creating a .mod file in the modules directory.

    Args:
        location: The path to the Maya preferences directory where the module
                  file should be installed.

    Returns:
        None
    """
    print(f"installing to {location}")
    current_dir = Path.cwd()
    mod_path = Path(location + f"modules/{MODULE_NAME}.mod")
    if mod_path.is_file():
        response = input(f"{mod_path} already exists. Replace? [y/N]: ").strip().lower()
        if response != "y":
            print("installation cancelled")
            return
    print("writing module file")
    with open(mod_path, "w") as file:
        file.write(f"+ {MODULE_NAME} 1.0 {current_dir}\n")
        file.write("MAYA_PLUG_IN_PATH +:= plug-ins\n")
        file.write("MAYA_SCRIPT_PATH +:= plug-ins/AETemplates\n")
        file.write("XBMLANGPATH +:= plug-ins/icons\n")


def check_maya_installed(op_sys: str) -> str:
    """
    Check if Maya is installed on the system and return its preferences location.
    Args:
        op_sys: The operating system name (e.g., 'Linux', 'Darwin', 'Windows').
    Returns:
        The path to the Maya preferences directory.
    Raises:
        FileNotFoundError: If the Maya preferences directory cannot be found.
    """
    mloc = f"{Path.home()}{maya_locations.get(op_sys)}/"
    if not Path(mloc).is_dir():
        raise FileNotFoundError(f"Maya installation not found at: {mloc}")
    return mloc


if __name__ == "__main__":
    op_sys = platform.system()
    try:
        m_loc = check_maya_installed(op_sys)
    except FileNotFoundError:
        print("Error can't find maya install")
        sys.exit(os.EX_CONFIG)

    install_module(m_loc)
