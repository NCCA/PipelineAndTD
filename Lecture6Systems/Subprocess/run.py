#!/usr/bin/env python

import sys


def main(num):
    for i in range(0, num):
        print(f"{i=}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
        print("Using command line args", file=sys.stderr)
    else:
        num = 10
    main(num)
