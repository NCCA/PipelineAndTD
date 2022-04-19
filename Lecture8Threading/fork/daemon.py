#!/usr/bin/env python
import os
import sys
import time


def daemonInit():
    # note use of := to assign value of fork to pid
    # https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions
    if (pid := os.fork()) < 0:
        return -1
    elif pid != 0:
        sys.exit(os.EX_OK)
    try:
        os.setsid()
    except PermissionError:
        print("pererror")
        pass
    return 0


if __name__ == "__main__":
    daemonInit()
    while True:
        print(f"ping {os.getpid()}")
        time.sleep(4)
