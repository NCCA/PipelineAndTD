#!/usr/bin/env python

import concurrent.futures
import logging
import random
import threading
import time

# create a global lock
g_lock = threading.Lock()


class SharedResource:
    def __init__(self):
        self.value = 0

    def update_resource(self, name, value):
        logging.info(f"Thread {name} starting")
        # simulate work with local variables to the class
        g_lock.acquire()  # no RAII
        logging.info(f"Thread {name} aquired lock")
        self.value += value
        time.sleep(random.uniform(0.1, 1))  # simulate work
        g_lock.release()
        logging.info(f"Thread {name} finishing update and releasing lock")


if __name__ == "__main__":
    format = "%(message)s : %(asctime)s "
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    num_threads = 12
    resource = SharedResource()
    total = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for index in range(num_threads):
            r = random.randint(10, 200)
            total += r
            logging.info(f"Updating theread {index} with value {r}")
            executor.submit(resource.update_resource, index, r)
    logging.info(f"Testing update. Ending value is {resource.value} should be {total}")
