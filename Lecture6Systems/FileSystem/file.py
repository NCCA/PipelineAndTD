#!/usr/bin/env python

import os
import random
import string

# grab our current directory
pwd = os.getcwd()
# first make a director called tmp and change into it
try:
    os.mkdir("tmp")
except FileExistsError:
    print("directory already exists")
os.chdir("tmp")

# make some random files note using the os.open method
# for demonstration purposes
for i in range(0, 10):
    file = os.open(f"tmpfile{i}.txt", os.O_RDWR | os.O_CREAT)
    rand_text = "".join(
        random.choices(
            string.ascii_uppercase + string.digits, k=random.randint(10, 200)
        )
    )
    os.write(file, rand_text.encode())
    os.close(file)
# change back to original directory and walk the subdirs
os.chdir(pwd)
# listdir gets a list
for file in os.listdir("tmp"):
    print(f"files {file}")

# scandir can be better as it returns a DirEntry
for file in os.scandir("tmp"):
    print(f"{file.name} {file.path}")
    print(f"{file.stat()}")
# Now tidy up
for file in os.scandir("tmp"):
    os.remove(file.path)
os.removedirs("tmp")
