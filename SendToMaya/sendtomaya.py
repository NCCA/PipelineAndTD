#!/usr/bin/env python

import argparse
import socket
import sys

def send_command(addr: tuple, command: str) -> None:
    """Send a command to Maya through a socket connection.
    
    Args:
        addr (tuple): Tuple containing host and port (host, port)
        command (str): The command to send to Maya
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(addr)
        client.sendall(command.encode("utf-8"))

def process_mel_command(command: str) -> str:
    """Process MEL command by joining lines and adding newline.
    
    Args:
        command (str): The MEL command to process
        
    Returns:
        str: Processed MEL command
    """
    return ' '.join(line.strip() for line in command.splitlines()) + '\n'

def setup_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description="""Send file to Maya on Port. Ensure the port is enabled and you have set the correct values. 
        echoOutput must be False for Maya 2022 else you get encode errors. To setup maya use the following:
        cmds.commandPort(name=":7002", sourceType="python", echoOutput=False)
        """
    )
    
    parser.add_argument(
        "--port", "-p",
        nargs="?",
        default=7890,
        type=int,
        help="command port to send on default 7890"
    )
    parser.add_argument(
        "--file", "-f",
        nargs="?",
        default="",
        type=str,
        help="file to send"
    )
    parser.add_argument(
        "--host", "-o",
        nargs="?",
        default="localhost",
        type=str,
        help="host, default localhost"
    )
    parser.add_argument(
        "--mel", "-m",
        action='store_true',
        help="sending a mel file as this needs different encoding"
    )
    
    return parser

def main() -> int:
    """Main function to process and send commands to Maya.
    
    Returns:
        int: Exit code
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r") as f:
            command = f.read()
    else:
        command = "".join(sys.stdin.readlines())
    
    if args.mel:
        print("Processing MEL command")
        command = process_mel_command(command)
    
    send_command((args.host, args.port), command)
    return 0

if __name__ == "__main__":
    sys.exit(main())