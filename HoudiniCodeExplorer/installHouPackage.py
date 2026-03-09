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


TOOLS = [
    {
        "name": "NCCA Code Explorer",
        "label": "Code Explorer",
        "icon": "CodeExplorer.png",
        "script": "shelf.py",
        "help": "Python Code Explorer for Houdini",
    }
]


def install_package(houdini_location, current_dir):
    # make package folder is it doesn't exist
    packages_folder = houdini_location / "packages"
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


def generate_shelf_xml(current_dir):
    """Generate the complete shelf XML with all tools."""
    # Build the member tools list
    member_tools = "\n    ".join(f'<memberTool name="{tool["name"]}"/>' for tool in TOOLS)
    # Build individual tool definitions
    tool_definitions = ""
    for tool in TOOLS:
        with open(f"{current_dir}/{tool['script']}", "r") as file:
            shelf_script = file.read()
        tool_definitions += f"""
  <tool name="{tool["name"]}" label="{tool["label"]}" icon="{str(current_dir)}/{tool["icon"]}">
    <script scriptType="python"><![CDATA[
{shelf_script}
    ]]></script>
    <helpText><![CDATA[
{tool["help"]}
    ]]></helpText>
  </tool>
"""

    shelf_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<shelfDocument>
  <!-- {PACKAGE_NAME} v{VERSION} Shelf Tools -->

  <!-- Define the shelf tab containing all tools -->
  <toolshelf name="codeexplorer" label="Code Explorer">
    {member_tools}
  </toolshelf>

  <!-- Individual tool definitions -->
{tool_definitions}
</shelfDocument>
"""
    return shelf_xml


def install_shelf(houdini_location, current_dir):
    """Install the shelf definition file."""
    toolbar_folder = houdini_location / "toolbar"
    toolbar_folder.mkdir(exist_ok=True, parents=True)

    shelf_xml = generate_shelf_xml(current_dir)
    shelf_file = toolbar_folder / f"{PACKAGE_NAME.lower()}.shelf"

    with open(shelf_file, "w") as file:
        file.write(shelf_xml)

    print(f"\n✓ Shelf file created at: {shelf_file}")
    print(f"  Contains {len(TOOLS)} tools:")
    for tool in TOOLS:
        print(f"    - {tool['label']}")


def check_houdini_installed(op_sys):
    houdini_location = Path(f"{Path.home()}{houdini_locations.get(op_sys)}")
    if not houdini_location.is_dir():
        raise FileNotFoundError(f"Houdini not found at {houdini_location}")
    return houdini_location


if __name__ == "__main__":
    try:
        op_sys = platform.system()
        houdini_location = check_houdini_installed(op_sys)
        current_dir = Path.cwd()

    except FileNotFoundError as e:
        print(f"Error can't find houdini install: {e}")
        sys.exit(-1)

    install_package(houdini_location, current_dir)
    install_shelf(houdini_location, current_dir)
