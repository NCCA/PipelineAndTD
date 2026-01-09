#!/usr/bin/env python
import concurrent.futures
import logging
import queue
import random
import signal
import string
import threading
import time

SENTINEL = object()


def randName():
    """
    generate a random name, in python3 we can use choices however in py2 we need a different version
    return ''.join(random.choice(string.ascii_letters)+(random.choice(string.ascii_letters + string.digits, k=random.randint(5, 20))))
    """
    return "".join(
        random.choice(string.ascii_letters)
        + (random.choice(string.ascii_letters + string.digits))
        for i in range(0, random.randint(5, 20))
    )


def producer(pipeline):
    while True:
        message = randName()
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")
        pipeline.set_message(SENTINEL, "Producer")

    # Send a sentinel message to tell consumer we're done


def consumer(pipeline):
    """Pretend we're saving a number in the database."""
    message = 0
    while True:  # message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)


class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    """

    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        return message

    def set_message(self, message, name):
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
