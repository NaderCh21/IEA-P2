# astar.py
import heapq 

def heuristic(a, b):
    """
    Computes the Manhattan distance between two points a and b.
    Used as the heuristic function for A* search.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_path(start, goal, grid):
    """
    Finds the shortest path from start to goal using the A* algorithm.
    """
    rows, cols = len(grid), len(grid[0])

    # Priority queue (min-heap) storing (f-score, g-score, position)
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))

    # Tracking path reconstruction
    came_from = {}
    g_score = {start: 0}  # Cost from start to each node
    closed_set = set()  # Nodes already processed

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        # If goal is reached, reconstruct and return the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return the path from start to goal

        closed_set.add(current)

        # Explore valid neighboring cells (Von Neumann neighborhood)
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy

            # Ensure within grid bounds
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue

            # Skip obstacles unless it's the goal
            if (nx, ny) != goal and grid[nx][ny] != 0:
                continue

            tentative_g = current_g + 1  # Cost from start to neighbor

            # Ignore nodes already processed with a better path
            if (nx, ny) in closed_set and tentative_g >= g_score.get((nx, ny), float('inf')):
                continue

            # If this path is better, record it and push to open set
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                f = tentative_g + heuristic((nx, ny), goal)
                heapq.heappush(open_set, (f, tentative_g, (nx, ny)))

    return None  # No valid path found
