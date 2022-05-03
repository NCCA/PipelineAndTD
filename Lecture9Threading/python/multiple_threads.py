#!/usr/bin/env python
import logging
import threading
import time

colours = {
    "red": "\x1B[31m",
    "green": "\x1B[32m",
    "yellow": "\x1B[33m",
    "blue": "\x1B[34m",
    "magenta": "\x1B[35m",
    "cyan": "\x1B[36m",
    "white": "\x1B[37m",
    "reset": "\033[0m",
}


def thread_function(name, colour):
    logging.info(f"{colour}Thread {name}: starting")
    time.sleep(2)
    logging.info(f"{colour}Thread {name}: finishing")


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    num_threads = 4
    threads = list()
    colour = ["red", "green", "yellow", "blue"]
    for i in range(num_threads):
        logging.info(f"creating thread{i}")
        thread = threading.Thread(
            target=thread_function,
            args=(f"Thread {i}", colours.get(colour[i])),
        )
        threads.append(thread)
        thread.start()

    for i, thread in enumerate(threads):
        logging.info(f"{colours.get(colour[i])}main joining thread {i}")
        thread.join()
        logging.info(f"{colours.get(colour[i])}main thread {i} done")
