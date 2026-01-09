#!/usr/bin/env -S uv run --active --script

import json
import platform
import sys
from pathlib import Path

houdini_version = "20.5"

houdini_locations = {
    "Linux": f"/houdini{houdini_version}/",
    "Darwin": f"/Library/Preferences/houdini/{houdini_version}",
    #    "Windows": "\\Documents\\maya\\", don't have a windows machine to test
}


PACKAGE_NAME = "TestUI"
VERSION = "1.0"
PYTHON_PATHS = "scripts"


def install_package(m_loc, current_dir):
    # make package folder is it doesn't exist
    packages_folder = m_loc / "packages"
    packages_folder.mkdir(exist_ok=True, parents=False)
    package = {}
    package["load_package_once"] = "true"
    # env is an array of items
    env = []
    item = dict()
    item["CUSTOM_ENV"] = str(current_dir)
    env.append(item)
    item = dict()
    item["PYTHONPATH"] = str(current_dir / PYTHON_PATHS)
    env.append(item)

    package["env"] = env
    with open(f"{packages_folder}/{PACKAGE_NAME}.json", "w") as file:
        json.dump(package, file, indent=2)
        print(json.dumps(package, indent=2))


def check_houdini_installed(op_sys):
    mloc = Path(f"{Path.home()}{houdini_locations.get(op_sys)}")
    if not mloc.is_dir():
        raise
    return mloc


if __name__ == "__main__":
    try:
        op_sys = platform.system()
        m_loc = check_houdini_installed(op_sys)
        current_dir = Path.cwd()

    except:
        print("Error can't find houdini install")
        sys.exit(-1)

    install_package(m_loc, current_dir)
