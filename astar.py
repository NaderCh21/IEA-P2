import heapq

def heuristic(a, b):
    """Manhattan distance between a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_path(start, goal, grid):
    """
    Returns a list of cells forming a path from start to goal if reachable; None if no path.
    grid[r][c] = 0 means free, nonzero means blocked unless it's the goal cell.
    """
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))

    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        closed_set.add(current)
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current[0]+dx, current[1]+dy
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
            if (nx, ny) != goal and grid[nx][ny] != 0:
                continue

            tentative_g = current_g + 1
            if (nx, ny) in closed_set and tentative_g >= g_score.get((nx, ny), float('inf')):
                continue

            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                f = tentative_g + heuristic((nx, ny), goal)
                heapq.heappush(open_set, (f, tentative_g, (nx, ny)))

    return None
