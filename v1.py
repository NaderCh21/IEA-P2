import pygame
import sys
from constants import CELL_SIZE, FPS, HEADER_HEIGHT, FOOTER_HEIGHT
from grid import initialize_grid, add_obstacles
from draw import draw_grid
from shape_selector import select_target_shape
from bfs import bfs_path

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 28)

grid_size = 10
input_text = str(grid_size)

def resize_screen(grid_size):
    return pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT))

screen = resize_screen(grid_size)
pygame.display.set_caption("Programmable Matter Grid")

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
        pygame.time.wait(100)

def move_elements_to_shape(grid, target_shape, screen):
    """Moves multiple elements sequentially to form the target shape."""
    current_positions = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    for current, target in zip(current_positions, target_shape):
        move_single_element(grid, current, target, screen)
    for target in target_shape:
        if grid[target[0]][target[1]] != 1:
            grid[target[0]][target[1]] = 1
            draw_grid(screen, grid)
            pygame.time.wait(300)

def main():
    global grid_size, screen, input_text

    grid = initialize_grid(grid_size)
    clock = pygame.time.Clock()
    
    while True:
        # Footer controls
        input_box = pygame.Rect(150, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 50, 30)
        apply_button = pygame.Rect(210, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 70, 30)

        # User shape selection + grid interaction
        selection = select_target_shape(grid, screen, CELL_SIZE, input_box, apply_button, input_text, font)

        if selection == "RESET":
            grid = initialize_grid(grid_size)
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

        # Valid target shape returned
        target_shape = selection

        # Add obstacles excluding the shape
        add_obstacles(grid, target_shape, obstacle_prob=0.1)

        # Move to target
        move_elements_to_shape(grid, target_shape, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
