#!/usr/bin/env python
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
    main(HOST, PORT)
