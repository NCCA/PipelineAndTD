#!/usr/bin/env python

import errno
import os

FIFO = "mypipe"

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

while True:
    with open(FIFO) as fifo:
        while True:
            data = fifo.read()
            if len(data) == 0:
                break
            print(f"{data}")
