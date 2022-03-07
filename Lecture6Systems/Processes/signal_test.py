#!/usr/bin/env python

import os
import signal
import time


def sig_handler(signum, frame):
    print(f"got signal {signum} {frame}")


if __name__ == "__main__":
    signal.signal(signal.SIGHUP, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    print(f"Running program pid is {os.getpid()}")
    while True:
        time.sleep(10)
        print(".")
