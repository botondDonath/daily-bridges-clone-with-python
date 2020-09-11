import unittest
from grid import Grid
from vector import Vector


class GridTest(unittest.TestCase):

    def test_neighbours_of_for_inner_cell(self):
        grid = Grid(10)
        pos = Vector(1, 1)
        expected = {
            "UP": grid.cell_at(Vector(0, 1)),
            "RIGHT": grid.cell_at(Vector(1, 2)),
            "DOWN": grid.cell_at(Vector(2, 1)),
            "LEFT": grid.cell_at(Vector(1, 0))
        }
        self.assertDictEqual(expected, grid.neighbours_of(pos))

    def test_neighbours_of_for_outer_cell(self):
        grid = Grid(10)
        pos = Vector(0, 1)
        expected = {
            "RIGHT": grid.cell_at(Vector(0, 2)),
            "DOWN": grid.cell_at(Vector(1, 1)),
            "LEFT": grid.cell_at(Vector(0, 0))
        }
        self.assertDictEqual(expected, grid.neighbours_of(pos))

    def test_neighbours_of_for_corner_cell(self):
        grid = Grid(10)
        pos = Vector(0, 0)
        expected = {
            "RIGHT": grid.cell_at(Vector(0, 1)),
            "DOWN": grid.cell_at(Vector(1, 0))
        }
        self.assertDictEqual(expected, grid.neighbours_of(pos))
