from grid import Grid, Cell


class GameGrid(Grid):

    def __init__(self, grid: Grid):
        super().__init__(grid.size)
        cells = grid.cells
        for r, row in enumerate(cells):
            for c, cell in enumerate(row):
                game_cell = GameCell(r, c, self)
                if cell.is_node():
                    game_cell.put_node()
                    game_cell.set_edges(cell.get_node().edges)
                self.cells[r][c] = game_cell


class GameCell(Cell):

    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)

    def set_edges(self, edges: dict):
        self.edges = {dir_key: None for dir_key, edge in edges.items()}
        self.edge_count = sum(map(lambda edge: edge.weight, edges.values()))

    def get_edge_count(self):
        return self.edge_count
