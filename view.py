from grid import Grid, Cell
from os import system


class Display:

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, grid: Grid):
        self.grid = grid

    def show_grid(self):
        self.clear()
        g = self.grid
        self.print_row("".join(map(lambda x: str(x).ljust(3), range(1, g.size + 1))))
        self.print_row(" ".ljust(3) * g.size)
        for r, row in enumerate(g.cells):
            self.print_row(
                "  ".join(self.convert_cell(cell) for cell in row),
                row_start=Display.ALPHABET[r] + " " * 3
            )

    def convert_cell(self, cell: Cell):
        if cell.is_empty():
            return "."
        if cell.is_node():
            return str(cell.get_edge_count())
        if cell.edge.direction.axis() == "x":
            return "|" if cell.edge.weight == 1 else u"\u2016"
        return "–" if cell.edge.weight == 1 else "="

    def print_row(self, row, row_start=None):
        row_start = " " * 4 if row_start is None else row_start
        print(row_start + row)

    def clear(self):
        system("clear")
