#!/usr/bin/env python

import os
import shutil

os.system("tar vfxz BaseMayaProject.tgz")

shutil.copytree("BaseMayaProject", "NewMayaProject")
shutil.rmtree("BaseMayaProject")
