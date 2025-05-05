import pygame
import sys
from constants import CELL_SIZE, FPS, HEADER_HEIGHT, FOOTER_HEIGHT
from grid import initialize_grid, add_obstacles, set_neighborhood, VON_NEUMANN_OFFSETS, MOORE_OFFSETS
from draw import draw_grid
from shape_selector import select_target_shape, draw_ui
from bfs import bfs_path

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 28)

grid_size = 20
input_text = str(grid_size)
neighborhood_mode = 'moore'

def resize_screen(grid_size):
    return pygame.display.set_mode(
        (grid_size * CELL_SIZE, grid_size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT)
    )

screen = resize_screen(grid_size)
pygame.display.set_caption("Programmable Matter Grid ----- Sequential Execution")

def main():
    global grid_size, screen, input_text, neighborhood_mode

    clock = pygame.time.Clock()
    steps_counter = 0

    # Initialize grid with agents at the bottom
    grid = initialize_grid(grid_size)
    for row in (grid_size - 1, grid_size - 2, grid_size - 3):
        for c in range(grid_size):
            grid[row][c] = 1

    target_shape = None

    # Target shape selection loop
    while target_shape is None:
        y_pos = grid_size * CELL_SIZE + HEADER_HEIGHT + 5
        win_w = screen.get_width()
        input_box_rect = pygame.Rect(win_w - 140, y_pos, 60, 30)
        apply_btn_rect = pygame.Rect(win_w - 70, y_pos, 60, 30)

        selection = select_target_shape(
            grid, screen, CELL_SIZE,
            input_box_rect, apply_btn_rect, input_text, font, steps_counter
        )

        if selection == "RESET":
            grid = initialize_grid(grid_size)
            for row in (grid_size - 1, grid_size - 2, grid_size - 3):
                for c in range(grid_size):
                    grid[row][c] = 1
            continue

        if isinstance(selection, tuple):
            if selection[0] == "APPLY":
                try:
                    new_size = int(selection[1])
                    if 4 <= new_size <= 50:
                        grid_size = new_size
                        input_text = str(grid_size)
                        screen = resize_screen(grid_size)
                        grid = initialize_grid(grid_size)
                        for row in (grid_size - 1, grid_size - 2, grid_size - 3):
                            for c in range(grid_size):
                                grid[row][c] = 1
                        continue
                except ValueError:
                    continue
            elif selection[0] == "TOPOLOGY":
                new_mode = selection[1]
                if new_mode in ("moore", "von_neumann"):
                    neighborhood_mode = new_mode
                    set_neighborhood(neighborhood_mode)
                    continue
        else:
            target_shape = selection
            add_obstacles(grid, target_shape, obstacle_prob=0.1)

    # Movement phase
    starts = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 1]
    pairs = list(zip(starts, target_shape))
    directions = VON_NEUMANN_OFFSETS if neighborhood_mode == 'von_neumann' else MOORE_OFFSETS

    for start, target in pairs:
        path = bfs_path(start, target, grid, directions)
        if not path:
            continue
        prev = path[0]
        for nxt in path[1:]:
            grid[prev[0]][prev[1]] = 0
            grid[nxt[0]][nxt[1]] = 1
            steps_counter += 1
            prev = nxt

            screen.fill((255, 255, 255))
            draw_grid(screen, grid)

            # Draw updated UI footer with steps count
            y_pos = grid_size * CELL_SIZE + HEADER_HEIGHT + 5
            win_w = screen.get_width()
            input_box_rect = pygame.Rect(win_w - 140, y_pos, 60, 30)
            apply_btn_rect = pygame.Rect(win_w - 70, y_pos, 60, 30)

            draw_ui(screen, "Custom", False, input_box_rect, apply_btn_rect, font, input_text, neighborhood_mode.title(), False, steps_counter)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            clock.tick(FPS)

    # Final display
    screen.fill((255, 255, 255))
    draw_grid(screen, grid)
    y_pos = grid_size * CELL_SIZE + HEADER_HEIGHT + 5
    win_w = screen.get_width()
    input_box_rect = pygame.Rect(win_w - 140, y_pos, 60, 30)
    apply_btn_rect = pygame.Rect(win_w - 70, y_pos, 60, 30)
    draw_ui(screen, "Custom", False, input_box_rect, apply_btn_rect, font, input_text, neighborhood_mode.title(), False, steps_counter)
    pygame.display.flip()

    # Idle loop
    while True:
        sel = select_target_shape(
            grid, screen, CELL_SIZE,
            input_box_rect, apply_btn_rect, input_text, font, steps_counter
        )

        if sel == "RESET":
            return main()
        if isinstance(sel, tuple):
            if sel[0] == "APPLY":
                try:
                    new_size = int(sel[1])
                    if 4 <= new_size <= 50:
                        grid_size = new_size
                        input_text = str(grid_size)
                        screen = resize_screen(grid_size)
                        return main()
                except ValueError:
                    continue
            elif sel[0] == "TOPOLOGY":
                new_mode = sel[1]
                if new_mode in ("moore", "von_neumann"):
                    neighborhood_mode = new_mode
                    set_neighborhood(neighborhood_mode)
                    continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
