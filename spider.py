from vector import Vector, Directions
from grid import Grid, Cell
from random import choice, randint
from utils import roll


class Spider:
    CHANCE_TO_PUT = 0.6

    def __init__(self, grid: Grid):
        self.grid = grid
        self.to_put = int(Grid.FILL_RATIO * self.grid.size ** 2)
        self.pos = Vector.random(self.grid.size)
        self.nodes = []
        self.put_node()
        self.dir = None

    @staticmethod
    def build_grid(grid_size: int):
        grid = Grid(grid_size)
        spider = Spider(grid)
        spider.weave()
        return grid

    def weave(self):
        failures = 0
        while len(self.nodes) < self.to_put:
            bounds = self.detect_bounds()
            edges = 0

            for dir_key, pos in bounds.items():
                if self.will_not_put():
                    continue

                node_cell = self.choose_node_cell(dir_key, pos)
                if node_cell is not None:
                    self.put_node(cell=node_cell)
                    self.cell().build_edge(node_cell, weight=randint(1, 2))
                    failures = 0
                    edges += 1

            failures += int(edges == 0)
            if failures == len(self.nodes) * 2:
                print(f"Failed to account for fill ratio: {len(self.nodes)}/{self.to_put}")
                return

            self.relocate()

    def detect_bounds(self) -> dict:
        self.mark_pos()

        bounds = {}
        for dir_key in Directions.keys():
            self.dir = Directions.vector(dir_key)
            self.advance()

            if self.cell() is None or not self.cell().is_empty():
                self.reset_pos()
                continue

            self.advance()
            bound = self.find_bound()
            if bound is not None:
                bounds[dir_key] = bound
            self.reset_pos()

        return bounds

    def find_bound(self):
        dist = 2
        while self.cell() is not None:
            if self.cell().is_node():
                return self.pos
            elif self.cell().is_edge():
                return self.pos - self.dir if dist > 2 else None
            self.advance()
            dist += 1
        return self.pos - self.dir if dist > 2 else None

    def will_not_put(self):
        return not roll(int(Spider.CHANCE_TO_PUT * 100))

    def choose_node_cell(self, dir_key: str, bound_pos: Vector):
        full_dist = int(abs(bound_pos - self.pos))
        dir_ = Directions.vector(dir_key)
        to_try = list(range(2, full_dist + 1))
        while len(to_try) > 0:
            dist = choice(to_try)
            cell = self.cell(pos=self.pos + dist * dir_)
            if cell.can_put_node():
                return cell
            to_try.remove(dist)
        return None

    def relocate(self):
        self.pos = choice(self.nodes).pos

    def advance(self, direction: Vector = None, by=1):
        self.pos += by * (direction if direction is not None else self.dir)

    def mark_pos(self):
        self.marked_pos = self.pos

    def reset_pos(self):
        self.pos = self.marked_pos

    def cell(self, pos=None) -> Cell:
        return self.grid.cell_at(self.pos if pos is None else pos)

    def put_node(self, pos=None, cell=None):
        cell = self.cell(pos=pos) if cell is None else cell
        cell.put_node()
        self.nodes.append(cell)
