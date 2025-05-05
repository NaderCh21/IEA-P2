# bfs.py
from collections import deque
from grid import VON_NEUMANN_OFFSETS, MOORE_OFFSETS

def bfs_path(start, goal, grid , directions):
    """
    Finds the shortest path from start to goal using BFS.
    The goal cell is allowed even if it is not empty.
    :param start: Tuple (row, col) for the starting position.
    :param goal: Tuple (row, col) for the goal position.
    :param grid: 2D list representing the grid.
    :return: List of tuples representing the path from start to goal.
    """
    rows, cols = len(grid), len(grid[0])



    #directions = VON_NEUMANN_OFFSETS            # -----------------TWEEK 
    #directions = MOORE_OFFSETS



    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                # Allow moving into the goal cell even if it is not 0
                if grid[nx][ny] == 0 or (nx, ny) == goal:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
    return []  # No path found
