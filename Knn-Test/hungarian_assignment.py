# optimal_assignment.py
import numpy as np
from scipy.optimize import linear_sum_assignment
from astar import astar_path

def optimal_assignment(grid, target_shape):

    # Step 1: Collect all active (1-filled) cells
    cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    if not cells:
        return []

    # Step 2: Build cost matrix using A* path lengths
    cost_matrix = np.array([
        [len(astar_path(cell, tgt, grid)) if astar_path(cell, tgt, grid) else float('inf') for tgt in target_shape]
        for cell in cells
    ], dtype=float)

    # Step 3: Remove fully unreachable columns (targets) and rows (cells)
    valid_targets = [target_shape[i] for i in np.where(~np.all(np.isinf(cost_matrix), axis=0))[0]]
    cost_matrix = cost_matrix[:, np.where(~np.all(np.isinf(cost_matrix), axis=0))[0]]
    valid_cells = [cells[i] for i in np.where(~np.all(np.isinf(cost_matrix), axis=1))[0]]
    cost_matrix = cost_matrix[np.where(~np.all(np.isinf(cost_matrix), axis=1))[0], :]

    if cost_matrix.size == 0:
        return []

    # Step 4: Trim to square matrix by removing worst row/col iteratively
    def trim_to_square(cm, vc, vt):
        while cm.shape[0] != cm.shape[1] and cm.size > 0:
            if cm.shape[0] > cm.shape[1]:  # More rows than columns
                worst_idx = np.argmax(np.min(cm, axis=1))  # Worst row index
                cm = np.delete(cm, worst_idx, axis=0)
                del vc[worst_idx]
            else:  # More columns than rows
                worst_idx = np.argmax(np.min(cm, axis=0))  # Worst column index
                cm = np.delete(cm, worst_idx, axis=1)
                del vt[worst_idx]
        return cm, vc, vt

    cost_matrix, valid_cells, valid_targets = trim_to_square(cost_matrix, valid_cells, valid_targets)

    if cost_matrix.size == 0:
        return []

    # Step 5: Perform Hungarian algorithm, removing worst row/col if necessary
    assignments = []
    while True:
        try:
            row_idx, col_idx = linear_sum_assignment(cost_matrix)
            assignments = [(valid_cells[r], valid_targets[c]) for r, c in zip(row_idx, col_idx) if cost_matrix[r, c] < float('inf')]
            break
        except ValueError:
            if cost_matrix.shape[0] == 0 or cost_matrix.shape[1] == 0:
                break
            # Remove worst row/column based on max min cost
            worst_row = np.argmax(np.min(cost_matrix, axis=1))
            worst_col = np.argmax(np.min(cost_matrix, axis=0))
            if np.min(cost_matrix, axis=1)[worst_row] >= np.min(cost_matrix, axis=0)[worst_col]:
                cost_matrix = np.delete(cost_matrix, worst_row, axis=0)
                del valid_cells[worst_row]
            else:
                cost_matrix = np.delete(cost_matrix, worst_col, axis=1)
                del valid_targets[worst_col]

            if cost_matrix.size == 0:
                break

    return assignments
