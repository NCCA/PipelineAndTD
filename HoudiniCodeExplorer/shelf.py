import sys

# This is for development mode only remove modules before re-importing
modules = ["CodeExplorer", "NodeTree", "PythonHighlighter", "HouTextEditor"]

if any(module in sys.modules for module in modules):
    # remove old modules when in dev mode
    for module in modules:
        if module in sys.modules:
            del sys.modules[module]

# Note this will auto run the module as I check from houdini and run package with
# if __name__ == "__main__" or "hou" in dir():
#    run_package()
import CodeExplorer
