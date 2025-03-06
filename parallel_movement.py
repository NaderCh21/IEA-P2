# parallel_movement.py
import pygame
from draw import draw_grid
from astar import astar_path
from hungarian_assignment import optimal_assignment

def move_elements_in_parallel(grid, target_shape, screen):
    """
    Repeatedly:
      1) Build a symmetrical partial-coverage cost matrix (hungarian_assignment).
      2) Gather BFS one-step moves in batch => no overwriting.
      3) Apply them simultaneously.
    Stops when no progress or shape is filled by real cells.
    """

    while True:
        # Check if shape is fully filled by existing cells
        all_filled = all(grid[t[0]][t[1]] == 1 for t in target_shape)
        if all_filled:
            break

        # Build assignments
        assignments = optimal_assignment(grid, target_shape)
        if not assignments:
            break  # no feasible moves => done

        moves_made = False
        occupied_positions = {
            (r, c) for r in range(len(grid))
                    for c in range(len(grid[r]))
                    if grid[r][c] == 1
        }
        pending_moves = []

        for (cell, target) in assignments:
            if cell == target:
                continue
            path = astar_path(cell, target, grid)
            if path and len(path) > 1:
                next_pos = path[1]
                # Move if next_pos not occupied
                if next_pos not in occupied_positions or next_pos == target:
                    pending_moves.append((cell, next_pos))
                    occupied_positions.add(next_pos)

        if not pending_moves:
            break

        # Apply batch moves
        for (old_pos, new_pos) in pending_moves:
            grid[old_pos[0]][old_pos[1]] = 0
            grid[new_pos[0]][new_pos[1]] = 1
            moves_made = True

        draw_grid(screen, grid)
        pygame.time.wait(500)

        if not moves_made:
            break

    # No forced fill => leftover targets remain empty if not enough or unreachable
