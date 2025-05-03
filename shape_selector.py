import pygame
from draw import draw_grid

# Predefined shapes
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
    
    "Diamond" : [(6, 10),       # top tip

                (7,  9), (7, 10), (7, 11),
                (8,  8), (8, 12),(8, 9) , (8, 10), (8, 11),
                (9,  7), (9, 13),(9, 8), (9, 9), (9, 10) , (9, 11) , (9, 12), 
                (10, 6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12), (10,13), (10,14), # widest row
                (11, 7), (11,13),(11,8), (11,9),(11,10),(11,11), (11,12),
                (12, 8), (12,12),(12,9),(12,10),(12,11),
                (13, 9), (13,11),(13,10),

                (14,10)],        # bottom tip],

    "Custom": []
}

HEADER_HEIGHT = 60
FOOTER_HEIGHT = 40
DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH = 20, 15, 120
BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT = 160, 15, 80, 30
MAX_CUSTOM_CELLS = 20

def draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text):
    # Dropdown
    pygame.draw.rect(screen, (200, 200, 200), (DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH, 30))
    pygame.draw.rect(screen, (0, 0, 0), (DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH, 30), 2)
    screen.blit(font.render(selected_shape, True, (0, 0, 0)), (DROPDOWN_X + 10, DROPDOWN_Y + 5))

    if dropdown_open:
        for i, option in enumerate(PREDEFINED_SHAPES.keys()):
            pygame.draw.rect(screen, (230, 230, 230),
                             (DROPDOWN_X, DROPDOWN_Y + 30 * (i + 1), DROPDOWN_WIDTH, 30))
            pygame.draw.rect(screen, (0, 0, 0),
                             (DROPDOWN_X, DROPDOWN_Y + 30 * (i + 1), DROPDOWN_WIDTH, 30), 2)
            screen.blit(font.render(option, True, (0, 0, 0)),
                        (DROPDOWN_X + 10, DROPDOWN_Y + 35 + (i * 30)))

    # Reset Button
    pygame.draw.rect(screen, (255, 100, 100), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    screen.blit(font.render("Reset", True, (255, 255, 255)), (BUTTON_X + 15, BUTTON_Y + 5))

    # Footer Input
    footer_y = screen.get_height() - FOOTER_HEIGHT + 5
    screen.blit(font.render("Grid Size:", True, (0, 0, 0)), (20, footer_y))

    pygame.draw.rect(screen, (255, 255, 255), input_box)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    screen.blit(font.render(input_text, True, (0, 0, 0)), (input_box.x + 5, input_box.y + 5))

    pygame.draw.rect(screen, (100, 255, 100), apply_button)
    pygame.draw.rect(screen, (0, 0, 0), apply_button, 2)
    screen.blit(font.render("Apply", True, (0, 0, 0)), (apply_button.x + 5, apply_button.y + 5))

def select_target_shape(grid, screen, cell_size, input_box, apply_button, input_text, font):
    selected_shape = "Pyramid"
    target_shape = PREDEFINED_SHAPES[selected_shape]
    dropdown_open = False
    limit_reached = False
    active_input = False

    draw_grid(screen, grid)
    draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text)
    pygame.display.flip()

    while True:
        event_occurred = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if input_box.collidepoint(mx, my):
                    active_input = True
                else:
                    active_input = False

                if BUTTON_X <= mx <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= my <= BUTTON_Y + BUTTON_HEIGHT:
                    return "RESET"

                if apply_button.collidepoint(mx, my):
                    return "APPLY", input_text

                if DROPDOWN_X <= mx <= DROPDOWN_X + DROPDOWN_WIDTH and DROPDOWN_Y <= my <= DROPDOWN_Y + 30:
                    dropdown_open = not dropdown_open
                    event_occurred = True

                if dropdown_open:
                    for i, option in enumerate(PREDEFINED_SHAPES.keys()):
                        if DROPDOWN_Y + 30 * (i + 1) <= my <= DROPDOWN_Y + 30 * (i + 2):
                            selected_shape = option
                            target_shape = PREDEFINED_SHAPES[selected_shape] if selected_shape != "Custom" else []
                            dropdown_open = False
                            event_occurred = True

                if selected_shape == "Custom":
                    row, col = (my - HEADER_HEIGHT) // cell_size, mx // cell_size
                    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                        if (row, col) not in target_shape:
                            if len(target_shape) < MAX_CUSTOM_CELLS:
                                target_shape.append((row, col))
                                limit_reached = False
                                event_occurred = True
                            else:
                                limit_reached = True
                                event_occurred = True

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode
                event_occurred = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and target_shape:
                return target_shape

        if event_occurred:
            screen.fill((255, 255, 255))
            draw_grid(screen, grid)
            draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text)
            for row, col in target_shape:
                pygame.draw.rect(screen, (200, 100, 0),
                                 (col * cell_size, row * cell_size + HEADER_HEIGHT, cell_size, cell_size), 3)
            pygame.display.flip()
