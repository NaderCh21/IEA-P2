#main.py
import pygame
import sys
from constants import CELL_SIZE, FPS, HEADER_HEIGHT, FOOTER_HEIGHT
from grid import initialize_grid
from draw import draw_grid
from shape_selector import select_target_shape
from Kmeans import move_elements_in_parallel
#from hierarchical import hierarchical_reconfigure_visual


pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 28)

grid_size = 10
input_text = str(grid_size)

def resize_screen(grid_size):
    return pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT))

screen = resize_screen(grid_size)
pygame.display.set_caption("Programmable Matter Grid")

def main():
    global grid_size, screen, input_text

    grid = initialize_grid(grid_size)
    clock = pygame.time.Clock()
    steps_counter = 0

    while True:
        input_box = pygame.Rect(150, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 50, 30)
        apply_button = pygame.Rect(210, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 70, 30)

        selection = select_target_shape(grid, screen, CELL_SIZE, input_box, apply_button, input_text, font)

        if selection == "RESET":
            grid = initialize_grid(grid_size)
            steps_counter = 0
            continue

        if isinstance(selection, tuple) and selection[0] == "APPLY":
            try:
                new_size = int(selection[1])
                if 4 <= new_size <= 50:
                    grid_size = new_size
                    input_text = str(grid_size)
                    screen = resize_screen(grid_size)
                    grid = initialize_grid(grid_size)
                    continue
            except:
                continue

        target_shape = selection
        steps_counter = move_elements_in_parallel(grid, target_shape, screen)
        #steps_counter = hierarchical_reconfigure_visual(grid, target_shape, screen)

        screen.fill((255, 255, 255))
        draw_grid(screen, grid)

        font_footer = pygame.font.Font(None, 36)
        footer_surface = font_footer.render(f"Total Steps: {steps_counter}", True, (0, 0, 0))
        screen.blit(footer_surface, (10, grid_size * CELL_SIZE + HEADER_HEIGHT - 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
