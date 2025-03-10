import pygame
from draw import draw_grid
from astar import astar_path
from hungarian_assignment import optimal_assignment

def move_elements_in_parallel(grid, target_shape, screen):
    """
    Moves cells in parallel using repeated Hungarian assignments.
    1) No cells vanish (collision logic with 2-swap detection).
    2) Cells already on target are NOT skipped, so they can move if it helps.
    3) We allow up to 10 consecutive "no move" iterations before giving up.
    4) After the main loop, we do a repeated single-step nudge so leftover cells
       can inch their way to the target multiple steps.
    """

    rows, cols = len(grid), len(grid[0])

    def shape_formed():
        return all(grid[r][c] == 1 for (r, c) in target_shape)

    max_stuck_iterations = 10
    stuck_count = 0

    while True:
        # If shape is already complete, stop
        if shape_formed():
            print("Shape fully formed!")
            break

        # 1) Compute new Hungarian assignments for all live cells
        assignments = optimal_assignment(grid, target_shape)
        if not assignments:
            print("No valid assignments. Stopping.")
            break

        # 2) Build next_step for each cell's assigned path (just the first hop)
        next_step = {}
        occupied = {(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1}

        for (cell, tgt) in assignments:
            path = astar_path(cell, tgt, grid)
            if path and len(path) > 1:
                next_step[cell] = path[1]

        if not next_step:
            # No cell can move at all this iteration
            stuck_count += 1
            print(f"No step moves possible (iteration {stuck_count}).")
            if shape_formed():
                break
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            # Otherwise, keep looping for more attempts
            continue

        # 3) Handle collisions: multiple cells wanting the same new position
        collisions = {}
        for oldpos, newpos in next_step.items():
            collisions.setdefault(newpos, []).append(oldpos)

        final_moves = {}

        def is_2swap(a, b):
            # Two-cell swap if a wants b's spot and b wants a's spot
            return (b in next_step) and (next_step[b] == a)

        for newpos, old_positions in collisions.items():
            if len(old_positions) == 1:
                # Only one cell wants newpos => no collision
                final_moves[old_positions[0]] = newpos
            elif len(old_positions) == 2:
                # Possibly a 2-swap
                a, b = old_positions
                if is_2swap(a, b):
                    # Let both swap
                    final_moves[a] = next_step[a]
                    final_moves[b] = next_step[b]
                else:
                    # Two cells want the same spot => pick one (tie-break)
                    chosen = min(old_positions, key=lambda p: p[0] + p[1])
                    final_moves[chosen] = newpos
            else:
                # 3+ cells want the same spot => pick exactly one
                chosen = min(old_positions, key=lambda p: p[0] + p[1])
                final_moves[chosen] = newpos

        if not final_moves:
            # All moves got dropped by collision resolution
            stuck_count += 1
            print(f"No step moves possible after collision resolution (iteration {stuck_count}).")
            if shape_formed():
                break
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            continue

        # 4) We do have valid moves => reset stuck counter
        stuck_count = 0

        # 5) Apply moves in batch
        for oldpos in final_moves:
            grid[oldpos[0]][oldpos[1]] = 0
        for oldpos, newpos in final_moves.items():
            grid[newpos[0]][newpos[1]] = 1

        # Draw and pause
        draw_grid(screen, grid)
        pygame.time.wait(500)

    # 6) Repeated single-step nudge:
    #    keep moving leftover cells one step at a time until no progress or shape formed
    changed = True
    while not shape_formed() and changed:
        changed = False
        leftover = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
        missing = [(r, c) for (r, c) in target_shape if grid[r][c] == 0]

        for cell in leftover:
            if shape_formed():
                break
            for tgt in missing:
                if grid[tgt[0]][tgt[1]] == 1:
                    continue  # already occupied
                path = astar_path(cell, tgt, grid)
                if path and len(path) > 1:
                    # Move one step closer
                    grid[cell[0]][cell[1]] = 0
                    grid[path[1][0]][path[1][1]] = 1
                    changed = True
                    # (Optional) update the display each small nudge:
                    # draw_grid(screen, grid)
                    # pygame.time.wait(300)
                    break

    if shape_formed():
        print("Shape fully formed after repeated nudges!")
    else:
        print("Stopped with shape not fully formed.")
