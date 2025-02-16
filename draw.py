# draw.py
import pygame
from constants import CELL_SIZE, WHITE, ORANGE, BLACK, GRID_SIZE

def draw_grid(screen, grid):
    """
    Draws the grid on the screen.
    :param screen: Pygame screen object.
    :param grid: 2D list representing the grid.
    """
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if grid[row][col] == 0:
                color = WHITE  # Empty
            elif grid[row][col] == 1:
                color = ORANGE  # Programmable matter
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()
