#!/usr/bin/env python

import subprocess

subprocess.run("./run.py")

subprocess.run(["./run.py", "11"])

output = subprocess.run(["./run.py", "2"], capture_output=True)
print("Captured output ")
print(output)
