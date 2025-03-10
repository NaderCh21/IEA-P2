import pygame
from constants import CELL_SIZE, WHITE, ORANGE, BLACK, GRID_SIZE

HEADER_HEIGHT = 60  # Define a fixed header height for the UI

def draw_grid(screen, grid):
    """
    Draws the grid on the screen, shifting it down to make space for the header.
    :param screen: Pygame screen object.
    :param grid: 2D list representing the grid.
    """
    screen.fill(WHITE)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + HEADER_HEIGHT  # Shift grid down by HEADER_HEIGHT
            
            if grid[row][col] == 0:
                color = WHITE  # Empty cell
            elif grid[row][col] == 1:
                color = ORANGE  # Programmable matter cell
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    pygame.display.flip()
