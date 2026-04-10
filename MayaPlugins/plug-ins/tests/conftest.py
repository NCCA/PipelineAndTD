"""Shared pytest fixtures for maya standalone modules"""

import maya.standalone
import pytest


@pytest.fixture(scope="session")
def maya_standalone():
    try:
        maya.standalone.initialize(name="python")

        print("initializing maya-standalone")

        yield
    finally:
        maya.standalone.uninitialize()
