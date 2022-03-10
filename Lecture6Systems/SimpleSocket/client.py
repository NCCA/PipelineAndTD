#!/usr/bin/env python
import argparse
import socket


def main(host, port):
    exit_loop = False
    while not exit_loop:
        data = input("enter some text HUP to kill >")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data.encode())
            received = s.recv(1024)

            print(f"{received=}")
        if data == "HUP":
            exit_loop = True


if __name__ == "__main__":
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    parser = argparse.ArgumentParser(description="Echo client")

    parser.add_argument(
        "--host",
        "-hs",
        nargs="?",
        const="127.0.0.1",
        default="127.0.0.1",
        type=str,
        help="hostname",
    )
    parser.add_argument(
        "--port",
        "-p",
        nargs="?",
        const=65432,
        default=65432,
        type=int,
        help="server port (non-privileged ports are > 1023)",
    )

    args = parser.parse_args()
    main(args.host, args.port)
