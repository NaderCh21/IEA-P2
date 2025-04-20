def initialize_grid(grid_size):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for row in range(grid_size - 2, grid_size):
        for col in range(grid_size):
            grid[row][col] = 1  # Programmable matter
    return grid

def add_obstacles(grid, target_shape, obstacle_prob=0.1):
    import random
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0 and (r, c) not in target_shape:
                if random.random() < obstacle_prob:
                    grid[r][c] = 2
    return grid
