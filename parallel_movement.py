import random
import math
import pygame
from draw import draw_grid
from astar import astar_path
from hungarian_assignment import optimal_assignment  # Hungarian algorithm

"""
Right Now decision making is centralized because : One call to greedy_assignment() 
function decides where cells end up at every iteration for all cells

Current Goal : Create Distributed Decision making 

- Local Views --> Giving each cell its own state + immediat eneighbors  (instead of full grid) 
- Neibghbor Messaging --> Instead of global same Hungarian call, have cells exchange data 
- Convergence protocol --> run few round until no cells conflict instead of computing optimum directly. More fluid

"""



# Centralized Decision Making Greedy Assignment Algorithm 

def greedy_assignment(grid, target_shape):
    """
    Assigns each current module cell to a target cell using a greedy strategy.
    Returns a list of (current_cell, target_cell) pairs.
    """
    # List all current module positions and target positions
    current_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    if not current_cells or not target_shape:
        return []
    assignments = []
    assigned_cells = set()
    assigned_targets = set()
    # Pre-compute distances (path lengths) from each cell to each target
    distances = []
    for cell in current_cells:
        for tgt in target_shape:
            path = astar_path(cell, tgt, grid)
            if path:  # reachable
                distances.append((len(path), cell, tgt))
    # Sort all possible pairs by distance (shortest first)
    distances.sort(key=lambda x: x[0])
    # Greedily assign the closest pairs without reusing cells or targets
    for dist, cell, tgt in distances:
        if cell in assigned_cells or tgt in assigned_targets:
            continue
        assignments.append((cell, tgt))
        assigned_cells.add(cell)
        assigned_targets.add(tgt)
    return assignments











# Distributed Decsion Making Greedy Assignment Algorithm 

def distributed_greedy_assignment(grid, target_shape):
    """
    Each cell independently picks its own nearest (reachable) target.
    No global conflict resolution here—truly local decisions.
    Returns a list of (cell, target) pairs, one per module.
    """
    # find all modules and targets
    current_cells = [(r, c)
                     for r in range(len(grid))
                     for c in range(len(grid[r]))
                     if grid[r][c] == 1]
    if not current_cells or not target_shape:
        return []

    assignments = []
    for cell in current_cells:
        best = None
        best_dist = float('inf')
        for tgt in target_shape:
            path = astar_path(cell, tgt, grid)
            if path and len(path) < best_dist:
                best_dist = len(path)
                best = tgt
        if best is not None:
            assignments.append((cell, best))
    return assignments





def stochastic_distributed_assignment(grid, target_shape, T=1.0):
    """
    For each module, sample a target by cost-softmin:
      P(tgt) ∝ exp(–distance(cell→tgt) / T)
    """
    current = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    assigns = []
    for cell in current:
        choices = []
        for tgt in target_shape:
            path = astar_path(cell, tgt, grid)
            if path:
                choices.append((tgt, len(path)))
        if not choices:
            continue
        # softmin weights
        weights = [math.exp(-dist/T) for (_, dist) in choices]
        total = sum(weights)
        probs  = [w/total for w in weights]
        targets = [tgt for (tgt, _) in choices]
        pick = random.choices(targets, weights=probs, k=1)[0]
        assigns.append((cell, pick))
    return assigns












def move_elements_in_parallel(grid, target_shape, screen, assignment_mode='Hungarian', movement_mode='Synchronous'):
    """
    Moves the modules in the grid toward the target_shape in parallel, according to the 
    selected assignment algorithm and movement mode. Returns the total number of steps.
    """
    steps = 0
    max_stuck_iterations = 10
    stuck_count = 0

    def shape_formed():
        """Check if all target cells are filled (shape is complete)."""
        return all(grid[r][c] == 1 for (r, c) in target_shape)

    while True:
        # Termination condition: target shape formed
        if shape_formed():
            print("Shape fully formed!")
            break

        # Step 1: Compute assignments based on selected algorithm
        if assignment_mode == 'Hungarian':
            assignments = optimal_assignment(grid, target_shape)
        elif assignment_mode == 'Distributed':  # Distributed Greedy Mode
            assignments = distributed_greedy_assignment(grid, target_shape)
        elif assignment_mode == 'Greedy': # Greedy mode
            assignments = greedy_assignment(grid, target_shape)
        elif assignment_mode == 'Stochastic':
            assignments = stochastic_distributed_assignment(grid, target_shape, T=1.0)
        if not assignments:
            print("No valid assignments. Stopping.")
            break

        # Step 2: For each assignment, plan one step along a path to the target
        next_step = {}
        for (cell, tgt) in assignments:
            path = astar_path(cell, tgt, grid)
            if path and len(path) > 1:
                next_step[cell] = path[1]  # next move toward target

        if not next_step:
            # No moves possible this iteration
            stuck_count += 1
            print(f"No moves possible (iteration {stuck_count}).")
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            continue

        # Step 3: Resolve collisions (agents targeting the same cell or swapping)
        collisions = {}
        for old_pos, new_pos in next_step.items():
            collisions.setdefault(new_pos, []).append(old_pos)
        final_moves = {}  # approved moves for this step

        def is_two_way_swap(a, b):
            """Check if two agents are attempting to swap positions."""
            return b in next_step and next_step[b] == a

        for new_pos, old_positions in collisions.items():
            if len(old_positions) == 1:
                # No collision: one agent moving into this new_pos
                final_moves[old_positions[0]] = new_pos
            elif len(old_positions) == 2 and is_two_way_swap(old_positions[0], old_positions[1]):
                # Two-way swap: allow both moves
                a, b = old_positions[0], old_positions[1]
                final_moves[a] = next_step[a]
                final_moves[b] = next_step[b]
            else:
                # Conflict: multiple agents want the same cell (not a simple swap)
                # Choose one agent (with smallest row+col as priority) to move this round
                chosen = min(old_positions, key=lambda p: p[0] + p[1])
                final_moves[chosen] = next_step[chosen]

        if not final_moves:
            # No moves after collision resolution
            stuck_count += 1
            print(f"No moves after collision resolution (iteration {stuck_count}).")
            if stuck_count >= max_stuck_iterations:
                print("Reached max stuck iterations. Stopping.")
                break
            continue

        # Step 4: Execute the moves based on the movement mode
        stuck_count = 0  # reset stuck counter since we are moving this iteration
        if movement_mode == 'Synchronous':
            # Move all selected agents simultaneously
            for old_pos in final_moves:
                grid[old_pos[0]][old_pos[1]] = 0
            for old_pos, new_pos in final_moves.items():
                grid[new_pos[0]][new_pos[1]] = 1
            steps += 1  # one synchronized step completed
            # Update the display after all moves
            draw_grid(screen, grid)
            pygame.time.wait(10)
        else:  # Asynchronous movement
            # Remove all moving agents from their old positions first (free up cells)
            moving_agents = list(final_moves.keys())
            for old_pos in moving_agents:
                grid[old_pos[0]][old_pos[1]] = 0
            # Optionally, small delay to visualize agents leaving (not strictly necessary)
            draw_grid(screen, grid)
            pygame.time.wait(50)
            # Move agents one by one to their new positions
            for old_pos, new_pos in final_moves.items():
                grid[new_pos[0]][new_pos[1]] = 1
                steps += 1  # count each individual move as a step
                draw_grid(screen, grid)
                pygame.time.wait(50)

        # Continue loop until shape formed or stuck
    # --- end of main loop ---

    # Step 5: (Optional) Final nudges if shape incomplete.
    # This tries to move any remaining modules into empty target spots one step at a time.
    changed = True
    while not shape_formed() and changed:
        changed = False
        # Identify remaining module positions and empty target positions
        current_positions = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
        empty_targets = [(r, c) for (r, c) in target_shape if grid[r][c] == 0]
        for cell in current_positions:
            if shape_formed():
                break
            for tgt in empty_targets:
                if grid[tgt[0]][tgt[1]] == 1:
                    continue  # skip already filled target
                path = astar_path(cell, tgt, grid)
                if path and len(path) > 1:
                    # Nudge one step toward this target
                    grid[cell[0]][cell[1]] = 0
                    grid[path[1][0]][path[1][1]] = 1
                    steps += 1
                    changed = True
                    draw_grid(screen, grid)
                    pygame.time.wait(10)
                    break

    # Print final status and return step count
    if shape_formed():
        print(f"Final shape formed in {steps} steps!")
    else:
        print(f"Stopped with shape incomplete. Steps taken: {steps}")
    return steps
