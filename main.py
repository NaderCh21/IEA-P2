### main.py with Initial Module Pool, Topology Toggle, and Pre-Selection Rendering
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

grid_size = 10
input_text = str(grid_size)
# Neighborhood toggle setup
neighborhood_mode = 'von_neumann'
set_neighborhood(neighborhood_mode)
neighborhood_button = pygame.Rect(
    300,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    120,
    30
)

def resize_screen(grid_size):
    return pygame.display.set_mode(
        (grid_size * CELL_SIZE,
         grid_size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT)
    )

screen = resize_screen(grid_size)
pygame.display.set_caption("Programmable Matter Grid - Parallel")

def main():
    global grid_size, screen, input_text, neighborhood_mode

    # Initialize grid and add module pool at bottom two rows (20 agents)
    grid = initialize_grid(grid_size)
    for row in (grid_size - 1, grid_size - 2):
        for c in range(grid_size):
            grid[row][c] = 1

    clock = pygame.time.Clock()
    steps_counter = 0
    target_shape = None

    # Phase 1: Render initial state and handle selection
    while target_shape is None:
        # Draw current grid and controls
        screen.fill((255, 255, 255))
        draw_grid(screen, grid)
        # Draw topology button
        pygame.draw.rect(screen, (200, 200, 200), neighborhood_button)
        label = font.render(
            'Topology: ' + ('V-N' if neighborhood_mode=='von_neumann' else 'Moore'),
            True, (0, 0, 0)
        )
        screen.blit(label, (neighborhood_button.x + 5, neighborhood_button.y + 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if neighborhood_button.collidepoint(event.pos):
                    neighborhood_mode = 'moore' if neighborhood_mode=='von_neumann' else 'von_neumann'
                    set_neighborhood(neighborhood_mode)
        # Shape selector handles its own blitting and events
        sel = select_target_shape(
            grid, screen, CELL_SIZE,
            pygame.Rect(150, grid_size*CELL_SIZE+HEADER_HEIGHT+5, 50, 30),
            pygame.Rect(210, grid_size*CELL_SIZE+HEADER_HEIGHT+5, 70, 30),
            input_text, font
        )
        if sel == 'RESET':
            grid = initialize_grid(grid_size)
            for row in (grid_size - 1, grid_size - 2):
                for c in range(grid_size): grid[row][c] = 1
            continue
        if isinstance(sel, tuple) and sel[0] == 'APPLY':
            try:
                new_size = int(sel[1]);
                if 4 <= new_size <= 50:
                    grid_size = new_size
                    input_text = str(grid_size)
                    screen = resize_screen(grid_size)
                    grid = initialize_grid(grid_size)
                    for row in (grid_size - 1, grid_size - 2):
                        for c in range(grid_size): grid[row][c] = 1
            except ValueError:
                pass
            continue
        # Valid shape selected
        target_shape = sel
        add_obstacles(grid, target_shape, obstacle_prob=0.1)

    # Phase 2: Run parallel movement in background
    done_event = threading.Event()
    steps_container = {'count': 0}
    def run_parallel():
        steps_container['count'] = move_elements_in_parallel(grid, target_shape, screen)
        done_event.set()
    thread = threading.Thread(target=run_parallel, daemon=True)
    thread.start()

    # Phase 3: Pump events (no redraw) until parallel movement completes
    while not done_event.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and neighborhood_button.collidepoint(event.pos):
                # allow toggling topology even during movement
                neighborhood_mode = 'moore' if neighborhood_mode=='von_neumann' else 'von_neumann'
                set_neighborhood(neighborhood_mode)
        pygame.time.wait(100)
        pygame.event.pump()

    steps_counter = steps_container['count']

    # Phase 4: Render final state once
    screen.fill((255, 255, 255))
    draw_grid(screen, grid)
    pygame.draw.rect(screen, (200, 200, 200), neighborhood_button)
    label = font.render(
        'Topology: ' + ('V-N' if neighborhood_mode=='von_neumann' else 'Moore'),
        True, (0, 0, 0)
    )
    screen.blit(label, (neighborhood_button.x + 5, neighborhood_button.y + 5))
    footer = pygame.font.Font(None, 36).render(
        f"Total Steps: {steps_counter}", True, (0, 0, 0)
    )
    screen.blit(footer, (10, grid_size*CELL_SIZE+HEADER_HEIGHT-5))
    pygame.display.flip()

    # Phase 5: Idle until quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
