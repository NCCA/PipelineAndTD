#!/usr/bin/env python

import concurrent.futures
import logging
import time


def thread_function(message):
    logging.info(f"starting")
    time.sleep(2)
    logging.info(f"finishing")


if __name__ == "__main__":
    format = "%(message)s : %(asctime)s "
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    num_threads = 12
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(thread_function, range(num_threads))
