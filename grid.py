# grid.py
from constants import GRID_SIZE

def initialize_grid():
    """
    Initializes the grid with the last two rows filled with programmable matter (orange).
    """
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE - 2, GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = 1  # Programmable matter
    return grid
