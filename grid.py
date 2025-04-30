import random

# Topology offsets
VON_NEUMANN_OFFSETS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
]
MOORE_OFFSETS = VON_NEUMANN_OFFSETS + [
    (1, 1), (1, -1), (-1, 1), (-1, -1),
]

# Current mode (default: Von Neumann)
_neighborhood_mode = 'von_neumann'

def set_neighborhood(mode: str):
    """
    Switches neighborhood mode. Options: 'von_neumann', 'moore'
    """
    global _neighborhood_mode
    if mode not in ('von_neumann', 'moore'):
        raise ValueError(f"Unknown neighborhood: {mode}")
    _neighborhood_mode = mode

def get_neighbors(pos, grid):
    """
    Returns list of empty neighbor cells for pos based on current mode.
    """
    offsets = VON_NEUMANN_OFFSETS if _neighborhood_mode == 'von_neumann' else MOORE_OFFSETS
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    r, c = pos
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

def initialize_grid(size):
    """
    Creates a size x size grid initialized to zero (empty).
    """
    return [[0 for _ in range(size)] for _ in range(size)]

def add_obstacles(grid, shape, obstacle_prob=0.1):
    """
    Fills grid cells not in shape with obstacles based on probability.
    Obstacle cells are marked with -1. Existing modules (value==1) are preserved.
    """
    rows, cols = len(grid), len(grid[0])
    shape_set = set(shape)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                # keep your placed modules
                continue
            if (r, c) in shape_set:
                grid[r][c] = 0
            elif random.random() < obstacle_prob:
                grid[r][c] = -1
            else:
                grid[r][c] = 0
