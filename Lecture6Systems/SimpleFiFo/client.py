#!/usr/bin/env python

import errno
import os

FIFO = "mypipe"

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

with open(FIFO, "w") as fifo:
    for i in range(0, 100):
        fifo.write(f"{i}")
