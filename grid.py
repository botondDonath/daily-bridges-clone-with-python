from enum import IntEnum
from vector import Vector, Directions


class CellType(IntEnum):
    EMPTY = 0
    NODE = 1
    EDGE = 2


class Grid:
    FILL_RATIO = 0.15

    def __init__(self, size):
        self.size = size
        self.cells = [[Cell(x, y, self) for y in range(size)] for x in range(size)]
        for row in self.cells:
            for cell in row:
                cell.compute_neighbours()
        # (cell.compute_neighbours() for row in self.cells for cell in row)

    def cell_at(self, pos: Vector):
        return self.cells[pos.x][pos.y] if self.is_within_bounds(pos) else None

    def is_within_bounds(self, pos: Vector):
        return pos.x >= 0 and pos.x < self.size and pos.y >= 0 and pos.y < self.size

    def neighbours_of(self, pos: Vector = None, cell=None):
        neighbours = {}
        pos = pos if pos is not None else cell.pos
        for dir_key in Directions.keys():
            nb_pos = pos + Directions.vector(dir_key)
            if self.is_within_bounds(nb_pos):
                neighbours[dir_key] = self.cell_at(nb_pos)
        return neighbours


class Cell:
    def __init__(self, x: int, y: int, grid: Grid):
        self.x = x
        self.y = y
        self.pos = Vector(x, y)
        self.grid = grid
        self.neighbours = {}
        self.type = CellType.EMPTY

    def __str__(self):
        return f"Cell({self.x},{self.y},{self.type})"

    def compute_neighbours(self):
        self.neighbours = self.grid.neighbours_of(cell=self)

    def is_empty(self):
        return self.type == CellType.EMPTY

    def is_node(self):
        return self.type == CellType.NODE

    def is_edge(self):
        return self.type == CellType.EDGE

    def get_node(self):
        return self.node if self.type == CellType.NODE else None

    def put_node(self):
        if self.type != CellType.NODE:
            self.node = Node(self)
            self.type = CellType.NODE

    def remove_node(self):
        del self.node
        self.type = CellType.EMPTY

    def put_edge(self, edge):
        self.edge = edge
        self.type = CellType.EDGE

    def build_edge(self, to_cell, weight=1):
        if self.type != CellType.NODE:
            raise Exception("Only nodes can build edges.")
        self.node.build_edge(to_cell, weight)

    def can_put_node(self):
        return not any(nb.is_node() for nb in self.neighbours.values())

    def get_edge_count(self):
        return sum(map(lambda edge: edge.weight, self.get_node().edges.values()))


class Node:
    def __init__(self, cell: Cell):
        self.cell = cell
        self.edges = {}

    def __str__(self):
        return f"Node({self.cell.x},{self.cell.y})"

    def build_edge(self, to_cell: Cell, weight=1):
        to_cell.put_node()

        edge = Edge(self.cell, to_cell, weight=weight)
        dir_key = Directions.key_for(edge.direction)

        self.edges[dir_key] = edge
        to_cell.get_node().edges[Directions.opposite_key(dir_key)] = edge

        pos = self.cell.pos + edge.direction
        while pos != to_cell.pos:
            cell = self.cell.grid.cell_at(pos)
            cell.put_edge(edge)
            pos += edge.direction


class Edge:
    def __init__(self, from_: Cell, to: Cell, weight=1):
        self.from_ = from_
        self.to = to
        self.weight = weight
        self.direction = Directions.from_vector(to.pos - from_.pos)

    def __str__(self):
        return f"Edge({self.from_},{self.to})"
