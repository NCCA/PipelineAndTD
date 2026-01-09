#!/usr/bin/env -S uv run --active --script

import random

import h5py


def write_data(n: int = 1000) -> None:
    """write a single layer of data to the file this is an array of n lists of floats"""
    points = [[random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)] for _ in range(0, n)]
    with h5py.File("points.hdf5", "w") as file:
        file.create_dataset("points", data=points)


def read_data() -> None:
    with h5py.File("points.hdf5", "r") as file:
        data = file["points"]
        print(data)
        # we can now slice the data
        print(data[:20])


def main() -> None:
    write_data()
    read_data()


if __name__ == "__main__":
    main()
