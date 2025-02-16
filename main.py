# main.py
import pygame
import sys
from constants import WINDOW_SIZE, FPS
from grid import initialize_grid
from draw import draw_grid
from bfs import bfs_path

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Programmable Matter Grid")

# Initialize grid
grid = initialize_grid()

# Predefined target shape (e.g., a square)
target_shape = [(4, 4), (4, 5), (5, 4), (5, 5)]  # 2x2 square

def move_single_element(grid, start, target, screen):
    """
    Moves a single element from its start to target position using BFS.
    """
    path = bfs_path(start, target, grid)
    if not path:
        print(f"No path found from {start} to {target}")
        return

    for next_pos in path:
        old_row, old_col = start
        grid[old_row][old_col] = 0  # Clear the old position
        grid[next_pos[0]][next_pos[1]] = 1  # Move to the new position
        start = next_pos

        # Redraw the grid to show the movement
        draw_grid(screen, grid)
        pygame.time.wait(300)  # Delay for smooth visualization


def move_elements_to_shape(grid, target_shape, screen):
    """
    Moves multiple elements to form a target shape sequentially using BFS.
    """
    # Get all current programmable matter positions
    current_positions = [
        (row, col) for row in range(len(grid)) for col in range(len(grid[row])) if grid[row][col] == 1
    ]

    # Sequentially move each cell to its target
    for current, target in zip(current_positions, target_shape):
        move_single_element(grid, current, target, screen)


def main():
    clock = pygame.time.Clock()

    # Move elements to form the target shape
    move_elements_to_shape(grid, target_shape, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
