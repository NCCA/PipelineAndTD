#!/usr/bin/env python
import pathlib

path = pathlib.Path.cwd()
print(path)
print(f"name is {path.name}")
Windows = pathlib.PureWindowsPath(r"C:\Users\jmacey/test.py")
print(Windows, type(Windows))
for p in pathlib.PurePosixPath(Windows).parts:
    print(p)

print(f"name is {Windows.name}")
print(f"suffixes {Windows.suffixes}")

# Join is useful

folder = pathlib.Path.home().joinpath("scripts", "test.py")
print(folder)
