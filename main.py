import pygame
import sys
from constants import WINDOW_SIZE, FPS, CELL_SIZE
from grid import initialize_grid
from draw import draw_grid
from shape_selector import select_target_shape
from parallel_movement import move_elements_in_parallel

HEADER_HEIGHT = 60  
FOOTER_HEIGHT = 40  # Add space for footer


pygame.init()
pygame.font.init() 
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT))  
pygame.display.set_caption("Programmable Matter Grid")
grid = initialize_grid()

def main():
    clock = pygame.time.Clock()

    steps_counter = 0  # Initialize before the loop

    while True:
        target_shape = select_target_shape(grid, screen, CELL_SIZE)  

        steps_counter = move_elements_in_parallel(grid, target_shape, screen)  # Get the step count
        print(f"DEBUG: Total Steps Received in Main = {steps_counter}")


        screen.fill((255, 255, 255))
        draw_grid(screen, grid)

        # Keep displaying the footer
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Total Steps: {steps_counter}", True, (0, 0, 0))
        screen.blit(text_surface, (10, WINDOW_SIZE + HEADER_HEIGHT - 30))  # Move slightly down


        pygame.display.flip()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
