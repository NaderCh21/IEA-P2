import numpy as np
from scipy.optimize import linear_sum_assignment
from astar import astar_path

def optimal_assignment(grid, target_shape):
    """
    Builds a cost matrix from *all* live cells to *all* target positions.
    Never fails: if Hungarian is infeasible, we remove the worst row/col and retry until success or empty.
    """

    # 1) Gather all live cells
    cells = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    if not cells:
        return []

    # 2) Build cost matrix
    cost_rows = []
    for cell in cells:
        row = []
        for tgt in target_shape:
            path = astar_path(cell, tgt, grid)
            row.append(len(path) if path else float('inf'))
        cost_rows.append(row)

    cost_matrix = np.array(cost_rows, dtype=float)

    # 3) Remove columns that are fully inf (unreachable targets *this* iteration)
    keep_cols = np.where(~np.all(np.isinf(cost_matrix), axis=0))[0]
    cost_matrix = cost_matrix[:, keep_cols]
    valid_targets = [target_shape[i] for i in keep_cols]

    # 4) Remove rows that are fully inf (cells that can't reach any target *this* iteration)
    keep_rows = np.where(~np.all(np.isinf(cost_matrix), axis=1))[0]
    cost_matrix = cost_matrix[keep_rows, :]
    valid_cells = [cells[i] for i in keep_rows]

    if cost_matrix.size == 0:
        return []

    # 5) Force a square matrix by trimming the dimension that is bigger
    def trim_to_square(cm, vc, vt):
        while True:
            rcount, ccount = cm.shape
            if rcount == 0 or ccount == 0:
                return cm, vc, vt
            if rcount == ccount:
                return cm, vc, vt
            if rcount > ccount:
                # remove row with worst min cost
                row_min = np.min(cm, axis=1)
                worst_idx = np.argmax(row_min)
                cm = np.delete(cm, worst_idx, axis=0)
                del vc[worst_idx]
            else:
                # remove col with worst min cost
                col_min = np.min(cm, axis=0)
                worst_idx = np.argmax(col_min)
                cm = np.delete(cm, worst_idx, axis=1)
                del vt[worst_idx]

    cost_matrix, valid_cells, valid_targets = trim_to_square(cost_matrix, valid_cells, valid_targets)
    if cost_matrix.size == 0:
        return []

    # 6) Repeatedly try linear_sum_assignment, removing the single worst row/col if it fails
    assignments = []
    while True:
        try:
            row_idx, col_idx = linear_sum_assignment(cost_matrix)
            for r, c in zip(row_idx, col_idx):
                if cost_matrix[r, c] < float('inf'):
                    assignments.append((valid_cells[r], valid_targets[c]))
            break
        except ValueError:
            rcount, ccount = cost_matrix.shape
            if rcount == 0 or ccount == 0:
                break
            # remove the worst row or col by max min cost
            row_min = np.min(cost_matrix, axis=1)
            col_min = np.min(cost_matrix, axis=0)
            worst_row = np.argmax(row_min)
            worst_col = np.argmax(col_min)
            if row_min[worst_row] >= col_min[worst_col]:
                # remove row
                cost_matrix = np.delete(cost_matrix, worst_row, axis=0)
                del valid_cells[worst_row]
            else:
                # remove col
                cost_matrix = np.delete(cost_matrix, worst_col, axis=1)
                del valid_targets[worst_col]
            if cost_matrix.size == 0:
                break

    return assignments
