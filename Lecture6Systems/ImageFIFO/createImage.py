#!/usr/bin/env python
import math
import random
import sys

sys.path.insert(0, "../ByteImage")
import ByteImage

if __name__ == "__main__":
    rx = random.randint
    img = ByteImage.ByteImage(800, 800, 255, 0, 0, 255)

    for i in range(0, 200):
        img.clear(255, 255, 255)
        cx = rx(1, img.width)
        cy = rx(1, img.height)
        for x in range(0, 1000):
            img.line(
                cx,
                cy,
                rx(1, img.width - 1),
                rx(1, img.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        sys.stderr.write(f"doing frame {i}\n")
        with open("imagefifo", "wb") as fifo:
            fifo.write(img.pixels)

        sys.stderr.flush()
        sys.stdout.flush()
