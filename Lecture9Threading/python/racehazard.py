#!/usr/bin/env python

import concurrent.futures
import logging
import random
import time


class SharedResource:
    def __init__(self):
        self.value = 0

    def update_resource(self, name, value):
        logging.info(f"Thread {name} starting update")
        # simulate work with local variables to the class
        local_value = self.value
        local_value += value
        time.sleep(random.uniform(0, 10))  # simulate work
        # now assign after work
        self.value = local_value
        logging.info(f"Thread {name} finishing update")


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
            # note the use of submit to pass values to the function
            executor.submit(resource.update_resource, index, r)
    logging.info(f"Testing update. Ending value is {resource.value} should be {total}")
