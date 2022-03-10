#!/usr/bin/env python

import errno
import os
import signal
import socket
import sys


def sig_handler(signum, frame):
    if signum in [signal.SIGHUP, signal.SIGINT]:
        print("stopping server")
        sys.exit(os.EX_OK)


def main(host, port):

    print(f"use ctrl + c to stop {os.getpid()}")

    signal.signal(signal.SIGHUP, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    exit_loop = False

    while not exit_loop:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if str(data.decode()) == "HUP":
                        exit_loop = True
                    print(f"{data=}")
                    if not data:
                        break
                    data = bytes(reversed(data))
                    conn.sendall(data)


if __name__ == "__main__":
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    main(HOST, PORT)
