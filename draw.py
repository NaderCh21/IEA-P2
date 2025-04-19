import pygame
from constants import CELL_SIZE, WHITE, ORANGE, BLACK, GRID_SIZE , RED



HEADER_HEIGHT = 60 

def draw_grid(screen, grid):

    screen.fill(WHITE)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + HEADER_HEIGHT  # Shift grid down by HEADER_HEIGHT
            
            if grid[row][col] == 0:
                color = WHITE  # Empty cell
            elif grid[row][col] == 1:
                color = ORANGE  # Programmable matter cell
            elif grid[row][col] == 2 : 
                color = RED # Obstacle color
            
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    pygame.display.flip()
