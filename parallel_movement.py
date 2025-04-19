# parallel_movement.py
import pygame
from draw import draw_grid
from astar import astar_path
from hungarian_assignment import optimal_assignment

def move_elements_in_parallel(grid, target_shape, screen):

    steps = 0
    rows, cols = len(grid), len(grid[0])
    max_stuck_iterations = 10  
    stuck_count = 0

    def shape_formed():
        """Checks if the grid matches the target shape."""
        return all(grid[r][c] == 1 for (r, c) in target_shape)

    while True:
        if shape_formed():
            print("Shape fully formed!")
            break

        # Step 1: Compute optimal assignments
        assignments = optimal_assignment(grid, target_shape)
        if not assignments:
            print("No valid assignments. Stopping.")
            break

        # Step 2: Determine the next movement step for each assigned cell
        next_step = {}
        for (cell, tgt) in assignments:
            path = astar_path(cell, tgt, grid)
            if path and len(path) > 1:
                next_step[cell] = path[1]  # Move one step towards target

        if not next_step:
            # No movement possible, increment stuck counter
            stuck_count += 1
            print(f"No moves possible (iteration {stuck_count}).")
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            continue

        # Step 3: Handle collisions where multiple cells want the same new position
        collisions = {}
        for oldpos, newpos in next_step.items():
            collisions.setdefault(newpos, []).append(oldpos)

        final_moves = {}

        def is_2swap(a, b):
            """Checks if two cells want to swap places."""
            return b in next_step and next_step[b] == a

        for newpos, old_positions in collisions.items():
            if len(old_positions) == 1:
                # No collision, move directly
                final_moves[old_positions[0]] = newpos
            elif len(old_positions) == 2 and is_2swap(*old_positions):
                # Allow two-way swaps
                final_moves[old_positions[0]] = next_step[old_positions[0]]
                final_moves[old_positions[1]] = next_step[old_positions[1]]
            else:
                # Conflict: select one cell to move based on row+col priority
                chosen = min(old_positions, key=lambda p: p[0] + p[1])
                final_moves[chosen] = newpos

        if not final_moves:
            # No moves after resolving collisions, increment stuck counter
            stuck_count += 1
            print(f"No moves after collision resolution (iteration {stuck_count}).")
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            continue

        # Step 4: Apply valid moves and reset stuck counter
        stuck_count = 0
        for oldpos in final_moves:
            grid[oldpos[0]][oldpos[1]] = 0
        for oldpos, newpos in final_moves.items():
            grid[newpos[0]][newpos[1]] = 1
        
        steps += 1 

        # Update the display
        draw_grid(screen, grid)
        pygame.time.wait(500)

    # Step 5: Repeated single-step nudges to move remaining cells
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
                    continue  # Skip occupied targets
                path = astar_path(cell, tgt, grid)
                if path and len(path) > 1:
                    # Move one step closer
                    grid[cell[0]][cell[1]] = 0
                    grid[path[1][0]][path[1][1]] = 1
                    changed = True
                    break

    print("Final shape formed!" if shape_formed() else "Stopping with shape incomplete.")
    print(f"Final shape formed in {steps} steps!" if shape_formed() else f"Stopping with shape incomplete. Steps taken: {steps}")

    return steps  # Return the total number of steps


