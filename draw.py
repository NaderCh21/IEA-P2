import pygame
from constants import CELL_SIZE, WHITE, ORANGE, BLACK, RED, HEADER_HEIGHT

def draw_grid(screen, grid):
    screen.fill(WHITE)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + HEADER_HEIGHT
            color = WHITE if grid[row][col] == 0 else ORANGE if grid[row][col] == 1 else RED
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()
