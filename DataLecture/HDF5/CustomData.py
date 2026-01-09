#!/usr/bin/env -S uv run --active --script

from __future__ import annotations

import random

import h5py


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def random(min: float = -1.0, max: float = 1.0) -> Vec3:
        return Vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))

    def to_list(self) -> List:
        return [self.x, self.y, self.z]

    def __str__(self) -> str:
        return f"[{self.x},{self.y},{self.z}]\n"

    def __repr__(self) -> str:
        return f"[{self.x},{self.y},{self.z}]\n"


def write_data(n: int = 1000) -> None:
    """write a single layer of data to the file this is an array of n lists of floats"""
    points = [Vec3.random(-10, 10).to_list() for _ in range(0, n)]
    with h5py.File("points.hdf5", "w") as file:
        file.create_dataset("points", data=points)


def read_data() -> None:
    with h5py.File("points.hdf5", "r") as file:
        data = file["points"]
        print(data)
        points = []
        for point in data:
            points.append(Vec3(point[0], point[1], point[2]))

        print(points[:10])


def main() -> None:
    write_data()
    read_data()


if __name__ == "__main__":
    main()
