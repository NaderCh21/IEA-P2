import pygame
import sys
from constants import WINDOW_SIZE, FPS, CELL_SIZE
from grid import initialize_grid
from draw import draw_grid
from shape_selector import select_target_shape
from parallel_movement import move_elements_in_parallel

HEADER_HEIGHT = 60  

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + HEADER_HEIGHT))  
pygame.display.set_caption("Programmable Matter Grid")
grid = initialize_grid()

def main():
    clock = pygame.time.Clock()

    while True:
        target_shape = select_target_shape(grid, screen, CELL_SIZE)  

        move_elements_in_parallel(grid, target_shape, screen)

        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
