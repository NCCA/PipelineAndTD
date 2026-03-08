#!/usr/bin/env hython

import json
import platform
import sys
from pathlib import Path

import hou

major_version = hou.getenv("HOUDINI_MAJOR_RELEASE")
minor_version = hou.getenv("HOUDINI_MINOR_RELEASE")
houdini_version = f"{major_version}.{minor_version}"


houdini_locations = {
    "Linux": f"/houdini{houdini_version}/",
    "Darwin": f"/Library/Preferences/houdini/{houdini_version}",
    #    "Windows": "\\Documents\\houdini\\", don't have a windows machine to test
}


PACKAGE_NAME = "CodeExplorer"
VERSION = "1.0"
PYTHON_PATHS = ""


def install_package(m_loc, current_dir):
    # make package folder is it doesn't exist
    packages_folder = m_loc / "packages"
    packages_folder.mkdir(exist_ok=True, parents=False)
    package = {}
    package["load_package_once"] = "true"
    # env is an array of items
    env = []
    item = dict()
    item["PYTHONPATH"] = str(current_dir / PYTHON_PATHS)
    env.append(item)

    package["env"] = env
    with open(f"{packages_folder}/{PACKAGE_NAME}.json", "w") as file:
        json.dump(package, file, indent=2)
        print(json.dumps(package, indent=2))


def check_houdini_installed(op_sys):
    houdini_location = Path(f"{Path.home()}{houdini_locations.get(op_sys)}")
    if not houdini_location.is_dir():
        raise
    return houdini_location


if __name__ == "__main__":
    try:
        op_sys = platform.system()
        houdini_location = check_houdini_installed(op_sys)
        current_dir = Path.cwd()

    except:
        print("Error can't find houdini install")
        sys.exit(-1)

    install_package(houdini_location, current_dir)
