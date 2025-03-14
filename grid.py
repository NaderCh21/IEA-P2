# grid.py
from constants import GRID_SIZE
import random

def initialize_grid():
    """
    Initializes the grid with the last two rows filled with programmable matter (orange).
    """
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE - 2, GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = 1  # Programmable matter
    return grid

# Obstacles generation function 
def add_obstacles(grid, target_shape, obstacle_prob=0.1):
    """
    Adds obstacles (value 2) to empty cells not in the target shape.
    """
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0 and (r, c) not in target_shape:
                if random.random() < obstacle_prob:
                    grid[r][c] = 2
    return grid