#!/usr/bin/env python

import errno
import os
import signal
import sys
from functools import partial

FIFO = "mypipe"


def main() :
    server_active=True

    try:
        os.mkfifo(FIFO)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise
    print(f"use ctrl + c to stop {os.getpid()}")

    def sig_handler(signum,frame) :
        nonlocal server_active
        if signum in [signal.SIGHUP,signal.SIGINT] :
            print(f"stopping server and removing fifo{server_active}")
            server_active=False

    signal.signal(signal.SIGHUP, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    while server_active :
        with open(FIFO) as fifo:
            while True and server_active:
                data = fifo.read()
                if len(data) == 0:
                    break
                print(f"{data}")
    os.remove(FIFO)




if __name__ == "__main__" :
 
    main()
