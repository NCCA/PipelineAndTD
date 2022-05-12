#!/usr/bin/env python
import logging
import threading
import time


def thread_function(name, colour):
    logging.info(f"{colour}{name}: starting")
    time.sleep(2)
    logging.info(f"{colour}{name}: finishing")


if __name__ == "__main__":

    format = "%(message)s : %(asctime)s "
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    num_threads = 4
    threads = list()
    colour = ["red", "green", "yellow", "blue"]
    for i in range(num_threads):
        logging.info(f"creating thread")
        thread = threading.Thread(
            target=thread_function,
            args=(f"Thread_{i}", f"\u001b[{i+30}m"),
        )
        threads.append(thread)
        thread.start()

    for i, thread in enumerate(threads):
        logging.info(f"\u001b[{i+30}mmain joining thread {i}")
        thread.join()
        logging.info(f"\u001b[{i+30}mmain thread {i} done")
