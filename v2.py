# v2.py
import pygame
import sys
from constants import WINDOW_SIZE, FPS, CELL_SIZE
from grid import initialize_grid
from draw import draw_grid
from astar import astar_path as bfs_path

from hungarian_assignment import optimal_assignment
from shape_selector import select_target_shape

def move_single_element(grid, start, target, screen):
    """Moves a single element from start to target using BFS."""
    path = bfs_path(start, target, grid)
    if not path:
        print(f"No path found from {start} to {target}")
        return
    for next_pos in path:
        grid[start[0]][start[1]] = 0
        grid[next_pos[0]][next_pos[1]] = 1
        start = next_pos
        draw_grid(screen, grid)
        pygame.time.wait(300)

def move_elements_to_shape(grid, target_shape, screen):
    """
    Moves multiple elements optimally using the Hungarian algorithm
    to form the target shape.
    """
    # Compute optimal assignments: a list of (current, target) pairs
    assignments = optimal_assignment(grid, target_shape)
    for current, target in assignments:
        move_single_element(grid, current, target, screen)
    
    # Ensure any remaining target cells are filled (e.g. inner cells)
    for target in target_shape:
        if grid[target[0]][target[1]] != 1:
            grid[target[0]][target[1]] = 1
            draw_grid(screen, grid)
            pygame.time.wait(300)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Programmable Matter Grid - Optimal Assignment")
    grid = initialize_grid()
    
    # Let the user define the target shape interactively
    target_shape = select_target_shape(grid, screen, CELL_SIZE)
    
    # Move elements optimally to form the target shape
    move_elements_to_shape(grid, target_shape, screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()
