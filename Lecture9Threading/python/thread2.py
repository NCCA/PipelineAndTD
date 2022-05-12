#!/usr/bin/env python
import logging
import threading
import time


def thread_function(name):
    logging.info(f"Thread {name}: starting")
    time.sleep(2)
    logging.info(f"Thread {name}: finishing")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S"
    )
    logging.info("In Main creating thread")
    thread = threading.Thread(target=thread_function, args=(1,), daemon=True)
    logging.info("Main starting thread")
    thread.start()
    # thread.join()
    logging.info("Main waiting for finish")
    logging.info("Main finished")
