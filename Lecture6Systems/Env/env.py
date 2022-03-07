#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":

    if os.environ.get("ENV_STARTUP") is None:
        print("Environment ENV_STARTUP not set")
        sys.exit(os.EX_CONFIG)
    else:
        print(f" working dir {os.environ['ENV_STARTUP']} ")
