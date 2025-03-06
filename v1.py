# main.py
import pygame
import sys
from constants import WINDOW_SIZE, FPS, CELL_SIZE
from grid import initialize_grid
from draw import draw_grid
from bfs import bfs_path
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
    """Moves multiple elements sequentially to form the target shape."""
    # Get all current programmable matter positions
    current_positions = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    
    # Move each element to its corresponding target cell
    for current, target in zip(current_positions, target_shape):
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
    pygame.display.set_caption("Programmable Matter Grid")
    grid = initialize_grid()

    # Let the user define the target shape interactively
    target_shape = select_target_shape(grid, screen, CELL_SIZE)
    
    # Move elements sequentially to form the selected shape
    move_elements_to_shape(grid, target_shape, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main()
    