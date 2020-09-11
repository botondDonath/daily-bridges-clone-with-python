import unittest
from grid import Grid
from spider import Spider
from vector import Vector


class SpiderTest(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(10)
        self.spider = Spider(self.grid)
        node_cell = self.spider.nodes[0]
        node_cell.remove_node()
        self.spider.nodes.clear()
        self.spider.pos = None

        '''
          0 1 2 3 4 5 6 7 8 9
        0 - - - - - - - - - -
        1 - - - - - - - - - -
        2 - - - - - - - - - -
        3 - - - - - - - - - -
        4 - - - - - - - - - -
        5 - - - - - - - - - -
        6 - - - - - - - - - -
        7 - - - - - - - - - -
        8 - - - - - - - - - -
        9 - - - - - - - - - -
        '''

    def test_choose_node_cell(self):
        self.spider.pos = Vector(0, 0)
        valid_cells = (Vector(0, 2), Vector(0, 3), Vector(0, 4))
        for _ in range(20):
            node_cell = self.spider.choose_node_cell("RIGHT", Vector(0, 4))
            self.assertIn(node_cell.pos, valid_cells)


class DetectBoundsTest(SpiderTest):

    def test_for_empty_grid(self):
        self.spider.pos = Vector(2, 2)
        expected = {
            "UP": Vector(0, 2),
            "RIGHT": Vector(2, 9),
            "DOWN": Vector(9, 2),
            "LEFT": Vector(2, 0)
        }
        self.assertDictEqual(expected, self.spider.detect_bounds())

    def test_for_grid_with_single_blocking_node(self):
        g = self.grid
        g.cell_at(Vector(1, 1)).put_node()
        self.spider.pos = Vector(2, 1)
        expected = {
            "RIGHT": Vector(2, 9),
            "DOWN": Vector(9, 1)
        }
        self.assertDictEqual(expected, self.spider.detect_bounds())

    def test_for_grid_with_single_non_blocking_node(self):
        g = self.grid
        g.cell_at(Vector(2, 8)).put_node()
        self.spider.pos = Vector(4, 8)
        expected = {
            "UP": Vector(2, 8),
            "DOWN": Vector(9, 8),
            "LEFT": Vector(4, 0)
        }
        self.assertDictEqual(expected, self.spider.detect_bounds())

    def test_for_grid_with_single_blocking_edge(self):
        g = self.grid
        c1 = g.cell_at(Vector(2, 2))
        c1.put_node()
        c2 = g.cell_at(Vector(2, 8))
        c1.build_edge(c2)

        self.spider.pos = Vector(4, 5)
        expected = {
            "DOWN": Vector(9, 5),
            "LEFT": Vector(4, 0),
            "RIGHT": Vector(4, 9)
        }
        self.assertDictEqual(expected, self.spider.detect_bounds())

    def test_for_grid_with_single_non_blocking_edge(self):
        g = self.grid
        c1 = g.cell_at(Vector(2, 2))
        c1.put_node()
        c2 = g.cell_at(Vector(2, 8))
        c1.build_edge(c2)

        self.spider.pos = Vector(5, 5)
        expected = {
            "UP": Vector(3, 5),
            "DOWN": Vector(9, 5),
            "LEFT": Vector(5, 0),
            "RIGHT": Vector(5, 9)
        }
        self.assertDictEqual(expected, self.spider.detect_bounds())

    def test_for_no_possible_bounds_in_corner(self):
        self.spider.pos = Vector(0, 0)
        g = self.grid
        g.cell_at(Vector(0, 1)).put_node()
        g.cell_at(Vector(1, 0)).put_node()
        self.assertDictEqual({}, self.spider.detect_bounds())

    def test_for_no_possible_bounds_for_inner_cell(self):
        self.spider.pos = Vector(4, 4)
        g = self.grid
        g.cell_at(Vector(3, 4)).put_node()
        g.cell_at(Vector(5, 4)).put_node()

        c1 = g.cell_at(Vector(2, 2))
        c1.put_node()
        c1.build_edge(g.cell_at(Vector(5, 2)))

        c2 = g.cell_at(Vector(2, 5))
        c2.put_node()
        c2.build_edge(g.cell_at(Vector(6, 5)))

        '''
          0 1 2 3 4 5 6 7 8 9
        0 - - - - - - - - - -
        1 - - - - - - - - - -
        2 - - X - - X - - - -
        3 - - # - X # - - - -
        4 - - # - * # - - - -
        5 - - X - X # - - - -
        6 - - - - - X - - - -
        7 - - - - - - - - - -
        8 - - - - - - - - - -
        9 - - - - - - - - - -
        '''

        self.assertDictEqual({}, self.spider.detect_bounds())
