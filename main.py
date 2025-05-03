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

# Initial parameters
grid_size = 20
input_text = str(grid_size)







# Topology toggle
neighborhood_mode = 'von_neumann'
set_neighborhood(neighborhood_mode)
neighborhood_button = pygame.Rect(
    10,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    120,
    30
)


# Assignment toggle (now with Distributed)            
assignment_modes = ['Hungarian', 'Greedy', 'Distributed']
assignment_mode = assignment_modes[0]  #--------------------- TWEEK 
assignment_button = pygame.Rect(
    140,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    140,
    30
)

# Movement toggle
movement_modes = ['Synchronous', 'Asynchronous']
movement_mode = movement_modes[0]  # --------------------------TWEEK 
movement_button = pygame.Rect(
    10,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    140,
    30
)

# Shape-selector buttons
reset_rect = pygame.Rect(
    450,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    50,
    30
)
apply_rect = pygame.Rect(
    510,
    grid_size * CELL_SIZE + HEADER_HEIGHT + 5,
    70,
    30
)

neighborhood_button = pygame.Rect(
    510,
    grid_size * CELL_SIZE + HEADER_HEIGHT - 10 ,
    70,
    30
)




def resize_screen(size):
    return pygame.display.set_mode(
        (size * CELL_SIZE,
         size * CELL_SIZE + HEADER_HEIGHT + FOOTER_HEIGHT)
    )

screen = resize_screen(grid_size)
pygame.display.set_caption("Programmable Matter Grid  ------   Parallel Execution  ")

def main():
    global grid_size, screen, input_text
    global neighborhood_mode, assignment_mode, movement_mode

    # Phase 0: Initialize grid
    grid = initialize_grid(grid_size)
    for row in (grid_size - 1, grid_size - 2):
        for c in range(grid_size):
            grid[row][c] = 1

    clock = pygame.time.Clock()
    steps_counter = 0
    target_shape = None



    # Phase 1: Configuration UI
    while target_shape is None:
        screen.fill((255, 255, 255))
        draw_grid(screen, grid)

        # Topology button
        pygame.draw.rect(screen, (200, 200, 200), neighborhood_button)
        topo_label = font.render(
            f"Topology: {'V-N' if neighborhood_mode=='von_neumann' else 'Moore'}",
            True, (0, 0, 0)
        )
        screen.blit(topo_label, (neighborhood_button.x + 5, neighborhood_button.y + 5))

        # Assignment button
        pygame.draw.rect(screen, (200, 200, 200), assignment_button)
        assign_label = font.render(f"Assign: {assignment_mode}", True, (0, 0, 0))
        screen.blit(assign_label, (assignment_button.x + 5, assignment_button.y + 5))

        # Movement button
        pygame.draw.rect(screen, (200, 200, 200), movement_button)
        move_label = font.render(f"Move: {movement_mode}", True, (0, 0, 0))
        screen.blit(move_label, (movement_button.x + 5, movement_button.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if neighborhood_button.collidepoint(mx, my):
                    neighborhood_mode = 'moore' if neighborhood_mode=='von_neumann' else 'von_neumann'
                    set_neighborhood(neighborhood_mode)
                elif assignment_button.collidepoint(mx, my):
                    idx = assignment_modes.index(assignment_mode)
                    assignment_mode = assignment_modes[(idx + 1) % len(assignment_modes)]
                elif movement_button.collidepoint(mx, my):
                    idx = movement_modes.index(movement_mode)
                    movement_mode = movement_modes[(idx + 1) % len(movement_modes)]
        

        
        # Pass control to shape selector
        sel = select_target_shape(
            grid, screen, CELL_SIZE,
            reset_rect, apply_rect,
            input_text, font, 
            
        )

        if sel == 'RESET':
            grid = initialize_grid(grid_size)
            for row in (grid_size - 1, grid_size - 2):
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

        target_shape = sel
        add_obstacles(grid, target_shape, obstacle_prob=0.1)

    # Phase 2: Run movement in background
    done_event = threading.Event()
    steps_container = {'count': 0}

    def run_parallel():
        steps_container['count'] = move_elements_in_parallel(
            grid, target_shape, screen,
            assignment_mode=assignment_mode,
            movement_mode=movement_mode
        )
        done_event.set()

    thread = threading.Thread(target=run_parallel, daemon=True)
    thread.start()

    # Phase 3: Wait, allow topology toggles
    while not done_event.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and neighborhood_button.collidepoint(event.pos):
                neighborhood_mode = 'moore' if neighborhood_mode=='von_neumann' else 'von_neumann'
                set_neighborhood(neighborhood_mode)
        pygame.time.wait(100)
        pygame.event.pump()

    steps_counter = steps_container['count']

    
    # Phase 4: Final display
    screen.fill((255, 255, 255))
    draw_grid(screen, grid)
    pygame.draw.rect(screen, (200, 200, 200), neighborhood_button) # Topology
    screen.blit(topo_label, (neighborhood_button.x + 5 , neighborhood_button.y + 5))
    pygame.draw.rect(screen, (200, 200, 200), assignment_button)
    screen.blit(assign_label, (assignment_button.x + 5, assignment_button.y + 5))
    pygame.draw.rect(screen, (200, 200, 200), movement_button)
    screen.blit(move_label, (movement_button.x + 5, movement_button.y + 5))
    footer = pygame.font.Font(None, 36).render(f"Total Steps: {steps_counter}", True, (0, 0, 0))
    screen.blit(footer, (10, grid_size * CELL_SIZE + HEADER_HEIGHT - 5))
    pygame.display.flip()
    



    # Phase 5: Idle
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
