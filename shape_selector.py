import pygame
from draw import draw_grid

# Define predefined shapes
PREDEFINED_SHAPES = {
    "Pyramid": [(5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1),
                (4, 7), (4, 6), (4, 5), (4, 4), (4, 3), (4, 2),
                (3, 6), (3, 5), (3, 4), (3, 3),
                (2, 5), (2, 4)],

    "Box": [(2, 7), (3, 7), (4, 7), (5, 7), (5, 6), (5, 5), (5, 4), (5, 3),
            (2, 3), (2, 4), (2, 5), (2, 6), (4, 6), (3, 6), (3, 5), (4, 5),
            (4, 4), (3, 4), (3, 3), (4, 3)],

    "Circular": [(6, 5), (6, 4), (5, 5), (5, 4), (5, 6), (5, 3), (4, 3), (4, 2),
                 (3, 2), (3, 3), (4, 6), (4, 7), (3, 7), (3, 6), (2, 6), (2, 5),
                 (2, 4), (1, 5), (1, 4), (2, 3)],

    "Custom": []  # User-defined shape
}

# **Initial state: Last two rows filled**
INITIAL_STATE = [(8, i) for i in range(10)] + [(9, i) for i in range(10)]

HEADER_HEIGHT = 60  
DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH = 20, 15, 120  
BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT = 160, 15, 80, 30 

# Added for cell selection limit 
MAX_CUSTOM_CELLS = 20 

def draw_ui(screen, selected_shape, dropdown_open , limit_reached = False):
    """Draws the dropdown and reset button in the header."""
    font = pygame.font.Font(None, 28)

    # Draw dropdown box
    pygame.draw.rect(screen, (200, 200, 200), (DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH, 30))
    pygame.draw.rect(screen, (0, 0, 0), (DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH, 30), 2)
    text_surface = font.render(selected_shape, True, (0, 0, 0))
    screen.blit(text_surface, (DROPDOWN_X + 10, DROPDOWN_Y + 5))

    # Draw dropdown options if open
    if dropdown_open:
        for i, option in enumerate(PREDEFINED_SHAPES.keys()):
            pygame.draw.rect(screen, (230, 230, 230), (DROPDOWN_X, DROPDOWN_Y + 30 * (i + 1), DROPDOWN_WIDTH, 30))
            pygame.draw.rect(screen, (0, 0, 0), (DROPDOWN_X, DROPDOWN_Y + 30 * (i + 1), DROPDOWN_WIDTH, 30), 2)
            option_text = font.render(option, True, (0, 0, 0))
            screen.blit(option_text, (DROPDOWN_X + 10, DROPDOWN_Y + 35 + (i * 30)))

    # Draw reset button
    pygame.draw.rect(screen, (255, 100, 100), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    reset_text = font.render("Reset", True, (255, 255, 255))

    screen.blit(reset_text, (BUTTON_X + 15, BUTTON_Y + 5))
    # Draw error message if limit reached when selecting pixels in custom mode 
    if limit_reached:
        error_font = pygame.font.Font(None, 24)
        error_text = error_font.render("Max 20 cells allowed!", True, (255, 0, 0))
        screen.blit(error_text, (DROPDOWN_X, DROPDOWN_Y + 40))

def select_target_shape(grid, screen, cell_size):
    """Handles shape selection and reset functionality."""
    selected_shape = "Pyramid"
    target_shape = PREDEFINED_SHAPES[selected_shape]
    dropdown_open = False

    screen.fill((255, 255, 255))
    draw_grid(screen, grid)
    draw_ui(screen, selected_shape, dropdown_open)
    pygame.display.flip()

    while True:
        event_occurred = False  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                    # Instantly reset the grid without showing movement
                    target_shape = INITIAL_STATE  
                    grid[:] = [[0] * len(grid[0]) for _ in range(len(grid))]  # Clear the grid
                    for row, col in INITIAL_STATE:
                        grid[row][col] = 1  # Fill the last two rows instantly

                    screen.fill((255, 255, 255))  
                    draw_grid(screen, grid)  
                    draw_ui(screen, selected_shape, dropdown_open)  
                    pygame.display.flip()  
                    return target_shape  


                if DROPDOWN_X <= mouse_x <= DROPDOWN_X + DROPDOWN_WIDTH and DROPDOWN_Y <= mouse_y <= DROPDOWN_Y + 30:
                    dropdown_open = not dropdown_open
                    event_occurred = True

                if dropdown_open:
                    for i, option in enumerate(PREDEFINED_SHAPES.keys()):
                        if DROPDOWN_X <= mouse_x <= DROPDOWN_X + DROPDOWN_WIDTH and DROPDOWN_Y + 30 * (i + 1) <= mouse_y <= DROPDOWN_Y + 30 * (i + 2):
                            selected_shape = option
                            target_shape = PREDEFINED_SHAPES[selected_shape] if selected_shape != "Custom" else []
                            dropdown_open = False
                            event_occurred = True

            # Custom shape selection

            if event.type == pygame.MOUSEBUTTONDOWN and selected_shape == "Custom":
                row, col = (event.pos[1] - HEADER_HEIGHT) // cell_size, event.pos[0] // cell_size
                if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                    if (row, col) not in target_shape:
                          if len(target_shape) < MAX_CUSTOM_CELLS:
                                target_shape.append((row, col))
                                event_occurred = True
                                limit_reached = False
                          else:
                            limit_reached = True
                            event_occurred = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and target_shape:
                return target_shape  

        if event_occurred:
            screen.fill((255, 255, 255))
            draw_grid(screen, grid)
            draw_ui(screen, selected_shape, dropdown_open)

            for row, col in target_shape:
                pygame.draw.rect(screen, (200, 100, 0), 
                                 (col * cell_size, row * cell_size + HEADER_HEIGHT, cell_size, cell_size), 3)

            pygame.display.flip()
