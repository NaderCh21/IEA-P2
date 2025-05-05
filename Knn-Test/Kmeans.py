# Kmeans.py
import pygame
from draw import draw_grid
from astar import astar_path
from hungarian_assignment import optimal_assignment
import numpy as np
from scipy.optimize import linear_sum_assignment
import random
import math

# (Optional) seed to stabilize K-means across runs
random.seed(42)

def kmeans(points, K, max_iters=50):
    pts = np.array(points, dtype=float)
    n = len(pts)
    K = min(K, n)
    if K <= 0:
        return [], []
    idx = random.sample(range(n), K)
    centroids = pts[idx]
    labels = np.zeros(n, dtype=int)
    for _ in range(max_iters):
        dists = np.linalg.norm(pts[:, None, :] - centroids[None, :, :], axis=2)
        new_labels = np.argmin(dists, axis=1)
        new_centroids = []
        for k in range(K):
            members = pts[new_labels == k]
            if len(members):
                new_centroids.append(members.mean(axis=0))
            else:
                new_centroids.append(pts[random.randrange(n)])
        new_centroids = np.vstack(new_centroids)
        if np.allclose(new_centroids, centroids):
            labels = new_labels
            break
        centroids, labels = new_centroids, new_labels
    int_centroids = [(int(round(r)), int(round(c))) for r, c in centroids]
    return labels.tolist(), int_centroids

def safe_astar(start, goal, grid, desc=""):
    """
    A* that in 'fallback' mode treats BOTH live cells (1) and obstacles (2)
    as blocked, ensuring paths curve around all occupied squares.
    """
    if desc.startswith("fallback"):
        # 0 = free, 2 = blocked (anything that's not 0)
        grid2 = [[2 if cell != 0 else 0 for cell in row] for row in grid]
    else:
        # only permanent obstacles (2) block
        grid2 = [[2 if cell == 2 else 0 for cell in row] for row in grid]
    return astar_path(start, goal, grid2)

def move_elements_in_parallel(grid, target_shape, screen, delay=300):
    rows, cols = len(grid), len(grid[0])
    steps = 0
    target_set = set(target_shape)

    def shape_formed():
        return all(grid[r][c] == 1 for r, c in target_shape)

    def resolve(proposals, fallback_mode=False):
        final = {}
        visited = set()
        # detect 2-cycles
        for u in list(proposals):
            if u in visited:
                continue
            path = []; v = u
            while v in proposals and v not in path:
                path.append(v)
                v = proposals[v]
            if v in path:
                cycle = path[path.index(v):]
                if len(cycle) == 2:
                    a, b = cycle
                    final[a] = proposals[a]
                    final[b] = proposals[b]
                    visited.update(cycle)
                else:
                    winner = min(cycle, key=lambda p: p[0] + p[1])
                    final[winner] = proposals[winner]
                    visited.update(cycle)
        # acyclic moves
        reserved = set(final.values())
        for old, new in sorted(proposals.items(), key=lambda it: it[0][0] + it[0][1]):
            if old in final:
                continue
            if new in reserved or grid[new[0]][new[1]] == 1:
                continue
            final[old] = new
            reserved.add(new)
        return final

    # 1. collect live cells
    cells = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]
    if not cells or not target_shape:
        return 0

        # 1b. require at least as many cells as targets
    if len(cells) < len(target_shape):
        raise ValueError(
            f"Need at least {len(target_shape)} live cells to fill all targets, "
            f"but only found {len(cells)}."
        )
    # otherwise, we have extra cells—those will simply remain once all targets are occupied


    # 2. cluster
    K = min(len(cells), len(target_shape), 5)
    labels_c, centroids_c = kmeans(cells, K)
    labels_t, centroids_t = kmeans(target_shape, K)

    # 3. match clusters
    cost = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            cr, cc = centroids_c[i]
            tr, tc = centroids_t[j]
            cost[i, j] = abs(cr - tr) + abs(cc - tc)
    row_ind, col_ind = linear_sum_assignment(cost)
    cluster_pairs = list(zip(row_ind.tolist(), col_ind.tolist()))

    # build per-cluster lists
    cluster_cells = [
        [cells[idx] for idx, lab in enumerate(labels_c) if lab == k]
        for k in range(K)
    ]

    # 4–5. hierarchical (one-axis, cardinal only)
    move_id = 0
    for ci, tj in cluster_pairs:
        while True:
            pts = cluster_cells[ci]
            cr = sum(r for r, _ in pts) / len(pts)
            cc = sum(c for _, c in pts) / len(pts)
            tr, tc = centroids_t[tj]

            if abs(tr - cr) >= abs(tc - cc):
                dr = int(math.copysign(1, tr - cr)) if abs(tr - cr) >= 1 else 0
                dc = 0
            else:
                dr = 0
                dc = int(math.copysign(1, tc - cc)) if abs(tc - cc) >= 1 else 0

            if dr == 0 and dc == 0:
                break

            proposals = {o: (o[0] + dr, o[1] + dc) for o in cluster_cells[ci]}
            moves = resolve(proposals)
            if not moves:
                print(f"⚠️ Hierarchical resolve stuck in cluster {ci}")
                break

            for o in moves:
                grid[o[0]][o[1]] = 0
            for o, n in moves.items():
                grid[n[0]][n[1]] = 1
            steps += 1
            move_id += 1
            print(f"Hier move {move_id}: cluster {ci} -> {moves}")

            cluster_cells[ci] = [moves.get(o, o) for o in cluster_cells[ci]]
            draw_grid(screen, grid)
            pygame.time.wait(delay)

    # 6. local nudge (4-neighborhood)
    nudge_id = 0
    while True:
        proposals = {}
        for ci, tj in cluster_pairs:
            tr, tc = centroids_t[tj]
            for o in cluster_cells[ci]:
                if o in target_set:
                    continue
                best = None
                best_d = abs(o[0] - tr) + abs(o[1] - tc)
                for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx, ny = o[0] + dr, o[1] + dc
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                        d = abs(nx - tr) + abs(ny - tc)
                        if d < best_d:
                            best_d, best = d, (nx, ny)
                if best:
                    proposals[o] = best
        if not proposals:
            break
        moves = resolve(proposals)
        if not moves:
            break

        for o in moves:
            grid[o[0]][o[1]] = 0
        for o, n in moves.items():
            grid[n[0]][n[1]] = 1
        steps += 1
        nudge_id += 1
        print(f"Local nudge {nudge_id}: {moves}")

        for ci, _ in cluster_pairs:
            cluster_cells[ci] = [moves.get(o, o) for o in cluster_cells[ci]]
        draw_grid(screen, grid)
        pygame.time.wait(delay)

    # 7. fallback (repeat until no proposals or done)
    print("Starting fallback…")
    while not shape_formed():
        assigns = optimal_assignment(grid, target_shape)
        prop = {}
        for cell, tgt in assigns:
            path = safe_astar(cell, tgt, grid, f"fallback {cell}->{tgt}")
            if path and len(path) > 1:
                prop[cell] = path[1]
        if not prop:
            break
        moves = resolve(prop, fallback_mode=True)
        if not moves:
            break
        for o in moves:
            grid[o[0]][o[1]] = 0
        for o, n in moves.items():
            grid[n[0]][n[1]] = 1
        steps += 1
        print(f"Fallback move: {moves}")
        draw_grid(screen, grid)
        pygame.time.wait(delay)

    # 8. serial fill using same safe_astar (blocks all occupied)
    missing = [t for t in target_shape if grid[t[0]][t[1]] == 0]
    for tgt in missing:
        # find path that goes around any 1 or 2
        p = safe_astar(
            min(
                [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1],
                key=lambda c: abs(c[0]-tgt[0]) + abs(c[1]-tgt[1])
            ),
            tgt,
            grid,
            "fallback"
        )
        if not p:
            continue
        for step_pos in p[1:]:
            # slide the cell along
            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == 1 and abs(r-step_pos[0])+abs(c-step_pos[1])==1:
                        grid[r][c], grid[step_pos[0]][step_pos[1]] = 0, 1
                        steps += 1
                        print(f"Serial fill: moved to {step_pos}")
                        draw_grid(screen, grid)
                        pygame.time.wait(delay)
                        break

    if shape_formed():
        print("✅ All targets reached.")
    else:
        print("❗ Some targets still missing")
    print(f"Finished. Steps: {steps}")
    return steps
