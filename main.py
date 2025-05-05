import pygame
import sys
import threading
from constants import CELL_SIZE, FPS, HEADER_HEIGHT, FOOTER_HEIGHT
from grid import initialize_grid, add_obstacles, set_neighborhood
from draw import draw_grid
from shape_selector import select_target_shape
from parallel_movement import move_elements_in_parallel

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 28)

# Modes and options
assignment_modes = ['Hungarian', 'Greedy', 'Distributed', 'Stochastic']
movement_modes = ['Synchronous', 'Asynchronous']


def draw_ui(screen, grid_size, neighborhood_mode, assignment_mode, movement_mode):
    """Draws styled UI buttons for topology, assignment, and movement modes."""
    y_ui = grid_size * CELL_SIZE + HEADER_HEIGHT + 10
    # Styling
    bg_color = (50, 50, 50)
    text_color = (255, 255, 255)
    btn_h = 30
    btn_w_nav = 140
    btn_w_assign = 160
    btn_w_move = 160
    padding = 10

    # Topology button
    topo_rect = pygame.Rect(padding, y_ui, btn_w_nav, btn_h)
    pygame.draw.rect(screen, bg_color, topo_rect, border_radius=5)
    topo_text = font.render(
        f"Topology: {'V-N' if neighborhood_mode=='von_neumann' else 'moore'}", True, text_color
    )
    screen.blit(topo_text, (topo_rect.x + 10, topo_rect.y + 5))

    # Assignment button
    assign_rect = pygame.Rect(padding*2 + btn_w_nav, y_ui, btn_w_assign, btn_h)
    pygame.draw.rect(screen, bg_color, assign_rect, border_radius=5)
    assign_text = font.render(f"Assign: {assignment_mode}", True, text_color)
    screen.blit(assign_text, (assign_rect.x + 10, assign_rect.y + 5))

    # Movement button
    move_rect = pygame.Rect(padding*3 + btn_w_nav + btn_w_assign, y_ui, btn_w_move, btn_h)
    pygame.draw.rect(screen, bg_color, move_rect, border_radius=5)
    move_text = font.render(f"Move: {movement_mode}", True, text_color)
    screen.blit(move_text, (move_rect.x + 10, move_rect.y + 5))

    return topo_rect, assign_rect, move_rect


def resize_screen(size):
    return pygame.display.set_mode(
        (size * CELL_SIZE,
         size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT)
    )

def draw_shape_selector(grid, screen, cell_size, input_text, font, grid_size, steps_counter):
    """
    Renders the shape‐selection UI (shape dropdown, Reset button,
    Grid Size input box, Apply button) and returns the selector’s return value.
    """
    # compute Y coordinate just below the grid
    y_pos = grid_size * cell_size + HEADER_HEIGHT + 5

    # position the input box & Apply button flush to the right edge
    win_w = screen.get_width()
    input_rect = pygame.Rect(win_w - 140, y_pos,  60, 30)
    apply_rect = pygame.Rect(win_w -  70, y_pos,  60, 30)

    # call into your existing selector logic
    return select_target_shape(
        grid, screen, cell_size,
        input_rect,      # location of the size‐input
        apply_rect,      # location of the Apply button
        input_text, font , steps_counter
    )


def main():
    # Initial parameters
    grid_size = 20
    input_text = str(grid_size)
    #neighborhood_mode = 'von_neumann'                             # ----------TWEEK
    neighborhood_mode = 'moore'
    steps_counter = 0

    #assignment_modes = ['Hungarian', 'Greedy', 'Distributed', 'Stochastic']
    #movement_modes = ['Synchronous', 'Asynchronous']
    assignment_mode = assignment_modes[0]                                   #-------------TWEEK
    movement_mode = movement_modes[0]

    
    screen = resize_screen(grid_size)
    pygame.display.set_caption("Programmable Matter Grid | Parallel Execution")

    clock = pygame.time.Clock()
    target_shape = None

    # Phase 0: Initialize grid
    grid = initialize_grid(grid_size)
    for row in (grid_size - 1, grid_size - 2, grid_size - 3):
        for c in range(grid_size):
            grid[row][c] = 1

    # Phase 1: Configuration UI
    while target_shape is None:
        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        topo_btn, assign_btn, move_btn = draw_ui(
            screen, grid_size, neighborhood_mode, assignment_mode, movement_mode
        )
        pygame.display.flip()

        # Handle toggles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if topo_btn.collidepoint(mx, my):
                    neighborhood_mode = 'moore' if neighborhood_mode == 'von_neumann' else 'von_neumann'
                    set_neighborhood(neighborhood_mode)
                elif assign_btn.collidepoint(mx, my):
                    idx = assignment_modes.index(assignment_mode)
                    assignment_mode = assignment_modes[(idx + 1) % len(assignment_modes)]
                elif move_btn.collidepoint(mx, my):
                    idx = movement_modes.index(movement_mode)
                    movement_mode = movement_modes[(idx + 1) % len(movement_modes)]

        # Shape selector (unchanged)
        # sel = select_target_shape(
        #     grid, screen, CELL_SIZE,
        #     pygame.Rect(450, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 50, 30),
        #     pygame.Rect(510, grid_size * CELL_SIZE + HEADER_HEIGHT + 5, 70, 30),
        #     input_text, font
        # )

        # Dynamically calculate position based on window width
        win_w = screen.get_width()
        y_pos = grid_size * CELL_SIZE + HEADER_HEIGHT + 5

        input_box_rect = pygame.Rect(win_w - 140, y_pos, 60, 30)
        apply_btn_rect = pygame.Rect(win_w - 70, y_pos, 60, 30)

        # Shape selector with dynamic positions
        sel = select_target_shape(
            grid, screen, CELL_SIZE,
            input_box_rect,
            apply_btn_rect,
            input_text, font, steps_counter
        ) 

         # handle topology‐dropdown first:
        if isinstance(sel, tuple) and sel[0] == "TOPOLOGY":
                neighborhood_mode = sel[1]             # "von_neumann" or "moore"
                set_neighborhood(neighborhood_mode)
                continue 

        if sel == 'RESET':
            grid = initialize_grid(grid_size)
            for row in (grid_size - 1, grid_size - 2, grid_size - 3):
                for c in range(grid_size):
                    grid[row][c] = 1
            continue
        if isinstance(sel, tuple) and sel[0] == 'APPLY':
            try:
                new_size = int(sel[1])
                if 4 <= new_size <= 50:
                    grid_size = new_size
                    input_text = str(grid_size)
                    screen = resize_screen(grid_size)
                    grid = initialize_grid(grid_size)
                    for row in (grid_size - 1, grid_size - 2):
                        for c in range(grid_size):
                            grid[row][c] = 1
            except ValueError:
                pass
            continue
        if isinstance(sel, list):  # only proceed if shape is selected

            target_shape = sel
        #add_obstacles(grid, target_shape, obstacle_prob=0.1)

    # Phase 2: Run movement in background
    done_event = threading.Event()
    steps_container = {'count': 0}
    add_obstacles(grid, target_shape, obstacle_prob=0.1)

    def run_parallel():
        set_neighborhood(neighborhood_mode)
        steps_container['count'] = move_elements_in_parallel(
            grid, target_shape, screen,
            assignment_mode=assignment_mode,
            movement_mode=movement_mode,
            neighborhood_mode=neighborhood_mode
        )
        done_event.set()
    threading.Thread(target=run_parallel, daemon=True).start()

    # Phase 3: Movement with real-time UI toggles
    while not done_event.is_set():
        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        topo_btn, assign_btn, move_btn = draw_ui(
            screen, grid_size, neighborhood_mode, assignment_mode, movement_mode
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if topo_btn.collidepoint(mx, my):
                    neighborhood_mode = 'moore' if neighborhood_mode == 'von_neumann' else 'von_neumann'
                    set_neighborhood(neighborhood_mode)

                elif assign_btn.collidepoint(mx, my):
                    idx = assignment_modes.index(assignment_mode)
                    assignment_mode = assignment_modes[(idx + 1) % len(assignment_modes)]
                elif move_btn.collidepoint(mx, my):
                    idx = movement_modes.index(movement_mode)
                    movement_mode = movement_modes[(idx + 1) % len(movement_modes)]
        clock.tick(FPS)

    steps_counter = steps_container['count']

    # ——————————————————————————————————————————————
# Phase 4+5: final display & idle — single loop
    while True:
        # 1) handle quit / pyramid / reset / apply clicks
        sel = draw_shape_selector(grid, screen, CELL_SIZE, input_text, font, grid_size , steps_counter)
        if sel == 'RESET':
            return main()   # restart from phase 1
        if isinstance(sel, tuple) and sel[0] == 'APPLY':
            try:
                new_size = int(sel[1])
                if 4 <= new_size <= 50:
                    grid_size = new_size
                    input_text = str(grid_size)
                    screen = resize_screen(grid_size)
                    grid = initialize_grid(grid_size)
                    for row in (grid_size-1, grid_size-2, grid_size-3):
                        for c in range(grid_size):
                            grid[row][c] = 1
                    return main()   # restart with new grid_size
            except ValueError:
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # 2) draw everything
        screen.fill((255,255,255))
        draw_grid(screen, grid)
        draw_ui(screen, grid_size, neighborhood_mode, assignment_mode, movement_mode)

        # steps footer
        footer = pygame.font.Font(None,36).render(
            f"Total Steps: {steps_counter}", True, (0,0,0)
        )
        screen.blit(footer, (10, grid_size*CELL_SIZE+HEADER_HEIGHT-5))

        # 3) flip & tick
        pygame.display.flip()
        clock.tick(FPS)
# ——————————————————————————————————————————————


if __name__ == '__main__':
    main()
