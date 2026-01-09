#!/usr/bin/env python
import logging
import random
import signal
import threading
import time


def thread_function(stop_event, name, colour):
    t = threading.currentThread()
    while not stop_event.wait(1):
        logging.info(f"{colour}{name}")
        time.sleep(random.randint(0, 10))
    logging.info(f"{colour}{name} Stopping")


if __name__ == "__main__":
    format = "%(message)s : %(asctime)s "
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    num_threads = 4
    stop_event = threading.Event()
    threads = []
    for i in range(num_threads):
        logging.info(f"creating thread")
        thread = threading.Thread(
            target=thread_function,
            args=(stop_event, f"Thread_{i}", f"\u001b[{i+31}m"),
        )
        threads.append(thread)
        thread.start()
    logging.info("killing threads")
    time.sleep(40)
    stop_event.set()

    for t in threads:
        t.join()
