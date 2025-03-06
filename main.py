# main.py
import pygame
import sys
from constants import WINDOW_SIZE, FPS, CELL_SIZE
from grid import initialize_grid
from draw import draw_grid
from shape_selector import select_target_shape
from parallel_movement import move_elements_in_parallel

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Programmable Matter Grid")
grid = initialize_grid()

def main():
    clock = pygame.time.Clock()
    
    # Let user define the target shape
    target_shape = select_target_shape(grid, screen, CELL_SIZE)
    
    # Parallel movement using updated code
    move_elements_in_parallel(grid, target_shape, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
