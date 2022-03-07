#!/usr/bin/env python
import math
import random
import sys

"""
Simple RGBA byte image with methods to write to stdout and ppm files
"""


class ByteImage:
    pixels = bytearray()

    def __init__(
        self, w: int, h: int, r: int = 255, g: int = 255, b: int = 255, a: int = 255
    ):
        """construct and set background colour"""
        self.width = w
        self.height = h
        self.pixels = bytearray([r, g, b, a] * (self.width * self.height))

    def set_pixel(self, x: int, y: int, r: int, g: int, b: int, a: int = 255):
        """set pixel at x,y with rgba value"""
        try:
            index = (self.width * y * 4) + x * 4
            self.pixels[index] = r
            self.pixels[index + 1] = g
            self.pixels[index + 2] = b
            self.pixels[index + 3] = a

        except ValueError:
            raise

    def clear(self, r, g, b, a=255):
        self.pixels = bytearray([r, g, b, a] * (self.width * self.height))

    def get_pixel(self, x: int, y: int):
        """get pixel values at x,y"""
        try:
            index = (self.width * y * 4) + x * 4
            r = self.pixels[index]
            g = self.pixels[index + 1]
            b = self.pixels[index + 2]
            a = self.pixels[index + 3]
            return r, g, b, a
        except ValueError:
            raise

    def random_pixels(self, alpha: int = 255):
        """fill buffer with random rgb values alpha to 255"""
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.set_pixel(
                    x,
                    y,
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    alpha,
                )

    def checker(
        self, r1: int, g1: int, b1: int, r2: int, g2: int, b2: int, check_size=10
    ):
        """simple checker pattern with 2 colours"""
        for y in range(0, self.height):
            for x in range(0, self.width):
                v = math.floor(check_size * x / self.width) + math.floor(
                    check_size * y / self.height
                )
                if v % 2 < 1.0:
                    self.set_pixel(x, y, r1, g1, b1)
                else:
                    self.set_pixel(x, y, r2, g2, b2)

    def write_ppm(self, name: str):
        """write to ppm for debug"""
        with open(name, "w") as file:
            file.write(f"P3\n{self.width} {self.height}\n255\n")
            for y in range(0, self.height):
                for x in range(0, self.width):
                    r, g, b, _ = self.get_pixel(x, y)
                    file.write(f"{r} {g} {b} \n")

    def line(self, x0, y0, x1, y1, r, g, b, a=255):
        """draw line from x1,y1 to x2,y2"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy
        while True:
            self.set_pixel(x0, y0, r, g, b, a)
            if (x0 == x1) and (y0 == y1):
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def to_stdout(self):
        """write whole buffer to stdout for pipe into ffmpeg etc"""
        sys.stdout.buffer.write(self.pixels)


if __name__ == "__main__":
    img = ByteImage(400, 400, 255, 0, 255, 255)
    img.random_pixels()
    img.write_ppm("test.ppm")
    img.checker(255, 0, 0, 255, 255, 255, 20)
    img.write_ppm("check.ppm")
    img.clear(255, 255, 255)
    rx = random.randint
    for i in range(0, 2000):
        img.line(
            rx(0, img.width - 1),
            rx(0, img.height - 1),
            rx(0, img.width - 1),
            rx(0, img.height - 1),
            rx(0, 255),
            rx(0, 255),
            rx(0, 255),
        )
    img.write_ppm("line.ppm")

    for i in range(0, 200):
        img.clear(255, 255, 255)
        cx = rx(0, img.width)
        cy = rx(0, img.height)
        for i in range(0, 2000):
            img.line(
                cx,
                cy,
                rx(0, img.width - 1),
                rx(0, img.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        img.to_stdout()
