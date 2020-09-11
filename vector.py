import random
import math


def other_axis(axis: str):
    return "y" if axis == "x" else "x"


class Vector(dict):
    def __init__(self, x: int, y: int, on_axis: str = None):
        super().__init__(self)
        if on_axis is None:
            on_axis = "x"

        self[on_axis] = x
        self[other_axis(on_axis)] = y
        self.x = self["x"]
        self.y = self["y"]

    def __str__(self):
        return f"Vector({self.x},{self.y})"

    @staticmethod
    def random(bound: int):
        return Vector(random.randrange(0, bound), random.randrange(0, bound))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: int):
        return self * other

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def axis(self):
        return "x" if abs(self.x) > abs(self.y) else "y"


class Directions:
    DIRECTIONS = {
        "UP": (Vector(-1, 0), "x0", "DOWN"),
        "RIGHT": (Vector(0, 1), "y1", "LEFT"),
        "DOWN": (Vector(1, 0), "x1", "UP"),
        "LEFT": (Vector(0, -1), "y0", "RIGHT")
    }
    ENCODED = {
        "x0": "UP",
        "y1": "RIGHT",
        "x1": "DOWN",
        "y0": "LEFT"
    }

    @staticmethod
    def keys():
        return Directions.DIRECTIONS.keys()

    @staticmethod
    def vector(dir_key: str):
        return Directions.DIRECTIONS[dir_key][0]

    @staticmethod
    def axis(dir_key: str):
        return Directions.DIRECTIONS[dir_key][1]

    @staticmethod
    def opposite_key(dir_key: str):
        return Directions.DIRECTIONS[dir_key][2]

    @staticmethod
    def key_for(vector: Vector):
        axis = vector.axis()
        code = axis + str(int(vector[axis] > 0))
        return Directions.ENCODED[code]

    @staticmethod
    def from_vector(vector: Vector):
        return Directions.vector(Directions.key_for(vector))

    @staticmethod
    def opposite(dir_key: str = None, vector: Vector = None):
        if dir_key is None:
            dir_key = Directions.key_for(vector)
        return Directions.vector(Directions.opposite_key(dir_key))
