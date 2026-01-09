#!/usr/bin/env -S uv run --active --script

import pickle


class Sphere:
    """A class to represent a sphere"""

    def __init__(self, name: str, x: float, y: float, z: float, radius: float = 1.0) -> None:
        """Initialize a sphere"""
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def __str__(self) -> str:
        """Return a string representation of a sphere"""
        return f"{self.name=} {self.x=} {self.y=} {self.z=} {self.radius=}"


if __name__ == "__main__":
    s = Sphere("test", 2.0, 0.0, 1.0, 2.3)

    with open("sphere", "wb") as file:
        pickle.dump(s, file)

    with open("sphere", "rb") as file:
        n = pickle.load(file)
        print(n)
