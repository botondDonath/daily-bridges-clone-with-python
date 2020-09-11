from unittest import TestCase
from vector import Vector, Directions


class DirectionTest(TestCase):

    def test_from_vector(self):
        params = (
            (Vector(5, 0), Directions.vector("DOWN")),
            (Vector(-2, 0), Directions.vector("UP")),
            (Vector(0, 6), Directions.vector("RIGHT")),
            (Vector(0, -4), Directions.vector("LEFT")),
        )
        for v, d in params:
            with self.subTest(msg=f"Testing for {v} and {d}", vector=v, direction=d):
                self.assertEquals(d, Directions.from_vector(v))
