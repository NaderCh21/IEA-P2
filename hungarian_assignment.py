import numpy as np
from scipy.optimize import linear_sum_assignment
from astar import astar_path

def optimal_assignment(grid, target_shape):
    """
    Builds an optimal assignment of current cells -> target_shape using BFS distances as costs.
    """

    # Step A: Gather current cells
    current_cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    if not current_cells:
        return []

    # Build cost matrix: rows = cells, columns = target positions
    cost_rows, filtered_cells = [], []
    for cell in current_cells:
        row_costs = [len(astar_path(cell, tgt, grid)) if astar_path(cell, tgt, grid) else float('inf') for tgt in target_shape]
        if not all(cost == float('inf') for cost in row_costs):
            cost_rows.append(row_costs)
            filtered_cells.append(cell)

    if not cost_rows:
        return []
    cost_matrix = np.array(cost_rows, dtype=float)

    # Step B: Remove columns that are all inf
    valid_cols = np.where(~np.all(np.isinf(cost_matrix), axis=0))[0]
    if len(valid_cols) == 0:
        return []
    cost_matrix = cost_matrix[:, valid_cols]
    filtered_targets = [target_shape[i] for i in valid_cols]

    if cost_matrix.size == 0:
        return []

    # Step C: Remove rows that are now all inf
    valid_rows = np.where(~np.all(np.isinf(cost_matrix), axis=1))[0]
    if len(valid_rows) == 0:
        return []
    cost_matrix = cost_matrix[valid_rows, :]
    final_cells = [filtered_cells[i] for i in valid_rows]

    if cost_matrix.size == 0:
        return []

    # Step D: Symmetrical partial coverage
    rows, cols = cost_matrix.shape
    if rows > cols:
        keep_rows = np.argsort(np.min(cost_matrix, axis=1))[:cols]
        cost_matrix = cost_matrix[keep_rows, :]
        final_cells = [final_cells[i] for i in keep_rows]
    elif cols > rows:
        keep_cols = np.argsort(np.min(cost_matrix, axis=0))[:rows]
        cost_matrix = cost_matrix[:, keep_cols]
        filtered_targets = [filtered_targets[i] for i in keep_cols]

    if cost_matrix.size == 0:
        return []

    # Step E: **Final check and removal of any all-inf rows/columns**
    while np.any(np.all(np.isinf(cost_matrix), axis=0)) or np.any(np.all(np.isinf(cost_matrix), axis=1)):
        # Remove all-inf rows
        valid_rows = np.where(~np.all(np.isinf(cost_matrix), axis=1))[0]
        if len(valid_rows) == 0:
            return []
        cost_matrix = cost_matrix[valid_rows, :]
        final_cells = [final_cells[i] for i in valid_rows]

        # Remove all-inf columns
        valid_cols = np.where(~np.all(np.isinf(cost_matrix), axis=0))[0]
        if len(valid_cols) == 0:
            return []
        cost_matrix = cost_matrix[:, valid_cols]
        filtered_targets = [filtered_targets[i] for i in valid_cols]

        if cost_matrix.size == 0:
            return []

    # Debugging: Print final cost matrix before Hungarian
    print("Final Cost Matrix (After Fixes):")
    print(cost_matrix)

    # Step F: Solve with Hungarian
    row_indices, col_indices = linear_sum_assignment(cost_matrix)

    # Step G: Build assignments
    assignments = [(final_cells[r_idx], filtered_targets[c_idx]) for r_idx, c_idx in zip(row_indices, col_indices) if cost_matrix[r_idx, c_idx] < float('inf')]

    return assignments
