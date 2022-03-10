#!/usr/bin/env python

import errno
import os
import signal
import sys

FIFO = "mypipe"


def sig_handler(signum, frame):
    if signum in [signal.SIGHUP, signal.SIGINT]:
        print("stopping server and removing fifo")
        os.remove(FIFO)
        sys.exit(os.EX_OK)


def main():

    try:
        os.mkfifo(FIFO)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise
    print(f"use ctrl + c to stop {os.getpid()}")

    signal.signal(signal.SIGHUP, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    while True:
        print("start while")
        with open(FIFO) as fifo:
            print("Open")
            while True:
                print("reading")
                data = fifo.read()
                print(f"read {len(data)} {type(data)}")
                if len(data) == 0:
                    print("break")
                    break
                print(f"out")


if __name__ == "__main__":

    main()
