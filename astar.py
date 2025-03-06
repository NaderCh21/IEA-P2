# astar.py
import heapq

def heuristic(a, b):
    """Calculate Manhattan distance between points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_path(start, goal, grid):
    """
    Returns a list of tuples representing the path from start to goal using A* search.
    Grid is a 2D list where 0 represents an empty cell, and any nonzero value is considered blocked.
    The goal cell is allowed even if it is not 0.
    If no path is found, returns an empty list.
    """
    rows, cols = len(grid), len(grid[0])
    open_set = []
    # Each entry in the heap is (f_score, g_score, position)
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    
    came_from = {}  # For path reconstruction
    g_score = {start: 0}
    closed_set = set()
    
    while open_set:
        current_f, current_g, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        closed_set.add(current)
        
        # Check neighbors (Von Neumann: up, down, left, right)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue  # Skip out-of-bound positions

            # Allow moving into the goal even if it's non-zero.
            if neighbor != goal and grid[neighbor[0]][neighbor[1]] != 0:
                continue

            tentative_g = current_g + 1
            if neighbor in closed_set and tentative_g >= g_score.get(neighbor, float('inf')):
                continue

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                
    return []  # No path found
