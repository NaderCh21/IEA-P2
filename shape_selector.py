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
    
    "Diamond L " : [(6, 10),       # top tip
                (7,  9), (7, 10), (7, 11),
                (8,  8), (8, 12),(8, 9) , (8, 10), (8, 11),
                (9,  7), (9, 13),(9, 8), (9, 9), (9, 10) , (9, 11) , (9, 12), 
                (10, 6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12), (10,13), (10,14), # widest row
                (11, 7), (11,13),(11,8), (11,9),(11,10),(11,11), (11,12),
                (12, 8), (12,12),(12,9),(12,10),(12,11),
                (13, 9), (13,11),(13,10),
                (14,10)],        # bottom tip],
    
    "Diamond XL ": [
        (0,10),
        (1,9), (1,10), (1,11),
        (2,8), (2,9), (2,10), (2,11), (2,12),
        (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (3,13),
        (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12), (4,13), (4,14),
        (5,5), (5,6), (5,7), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13), (5,14), (5,15),
        (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10), (6,11), (6,12), (6,13), (6,14), (6,15), (6,16),
        (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9), (7,10), (7,11), (7,12), (7,13), (7,14), (7,15), (7,16), (7,17),
        (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9), (8,10), (8,11), (8,12), (8,13), (8,14), (8,15), (8,16), (8,17), (8,18),
        (9,3), (9,4), (9,5), (9,6), (9,7), (9,8), (9,9), (9,10), (9,11), (9,12), (9,13), (9,14), (9,15), (9,16), (9,17),
        (10,4), (10,5), (10,6), (10,7), (10,8), (10,9), (10,10), (10,11), (10,12), (10,13), (10,14), (10,15), (10,16),
        (11,5), (11,6), (11,7), (11,8), (11,9), (11,10), (11,11), (11,12), (11,13), (11,14), (11,15),
        (12,6), (12,7), (12,8), (12,9), (12,10), (12,11), (12,12), (12,13), (12,14),
        (13,7), (13,8), (13,9), (13,10), (13,11), (13,12), (13,13),
        (14,8), (14,9), (14,10), (14,11), (14,12),
        (15,9), (15,10), (15,11),
        (16,10)
    ],

    "Border": [
        (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (0,10), (0,11), (0,12), (0,13), (0,14), (0,15), (0,16), (0,17), (0,18), (0,19),
        (16,0), (16,1), (16,2), (16,3), (16,4), (16,5), (16,6), (16,7), (16,8), (16,9), (16,10), (16,11), (16,12), (16,13), (16,14), (16,15), (16,16), (16,17), (16,18), (16,19),
        (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (11,0), (12,0), (13,0), (14,0), (15,0),
        (1,19), (2,19), (3,19), (4,19), (5,19), (6,19), (7,19), (8,19), (9,19), (10,19), (11,19), (12,19), (13,19), (14,19), (15,19)
    ],

    "Big Plus": [
        (1,10), (2,10), (3,10), (4,10), (5,10), (6,10), (7,10), (8,10), (9,10), (10,10), (11,10), (12,10), (13,10), (14,10), (15,10), (16,10),
        (10,1), (10,2), (10,3), (10,4), (10,5), (10,6), (10,7), (10,8), (10,9), (10,11), (10,12), (10,13), (10,14), (10,15), (10,16), (10,17), (10,18)
    ],

    "Big X": [
        (0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12), (13,13), (14,14), (15,15), (16,16),
        (0,19), (1,18), (2,17), (3,16), (4,15), (5,14), (6,13), (7,12), (8,11), (9,10), (10,9), (11,8), (12,7), (13,6), (14,5), (15,4), (16,3)
    ],


    "Custom": []
}

HEADER_HEIGHT = 60
FOOTER_HEIGHT = 40
DROPDOWN_X, DROPDOWN_Y, DROPDOWN_WIDTH = 20, 15, 120
BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT = 160, 15, 80, 30
MAX_CUSTOM_CELLS = 40

TOPOLOGY_DROPDOWN_X, TOPOLOGY_DROPDOWN_Y, TOPOLOGY_DROPDOWN_WIDTH = 250, 15, 120
topology_options = ["Von Neumann", "Moore"]
selected_topology = "Moore"
topology_dropdown_open = False



def draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text, selected_topology, topology_dropdown_open, steps_counter):
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

    # Topology Dropdown
    pygame.draw.rect(screen, (180, 180, 255), (TOPOLOGY_DROPDOWN_X, TOPOLOGY_DROPDOWN_Y, TOPOLOGY_DROPDOWN_WIDTH, 30))
    pygame.draw.rect(screen, (0, 0, 0), (TOPOLOGY_DROPDOWN_X, TOPOLOGY_DROPDOWN_Y, TOPOLOGY_DROPDOWN_WIDTH, 30), 2)
    screen.blit(font.render(selected_topology, True, (0, 0, 0)), (TOPOLOGY_DROPDOWN_X + 10, TOPOLOGY_DROPDOWN_Y + 5))

    if topology_dropdown_open:
        for i, option in enumerate(topology_options):
            rect = pygame.Rect(TOPOLOGY_DROPDOWN_X, TOPOLOGY_DROPDOWN_Y + 30 * (i + 1), TOPOLOGY_DROPDOWN_WIDTH, 30)
            pygame.draw.rect(screen, (230, 230, 255), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            screen.blit(font.render(option, True, (0, 0, 0)), (rect.x + 10, rect.y + 5))



    # Footer Input
    footer_y = screen.get_height() - FOOTER_HEIGHT + 5
    # Render Total Steps
    footer_steps_label = font.render(f"Total Steps: {steps_counter}", True, (0, 0, 0))
    steps_label_width = footer_steps_label.get_width()

    # Position it 20px from the right edge of the *visible screen*
    screen.blit(footer_steps_label, (screen.get_width() - steps_label_width - 450, footer_y))


    grid_size_label = font.render("Grid Size:", True, (0, 0, 0))
    screen.blit(grid_size_label, (input_box.left - grid_size_label.get_width() - 10, footer_y))

    pygame.draw.rect(screen, (255, 255, 255), input_box)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    screen.blit(font.render(input_text, True, (0, 0, 0)), (input_box.x + 5, input_box.y + 5))

    pygame.draw.rect(screen, (100, 255, 100), apply_button)
    pygame.draw.rect(screen, (0, 0, 0), apply_button, 2)
    screen.blit(font.render("Apply", True, (0, 0, 0)), (apply_button.x + 5, apply_button.y + 5))

def select_target_shape(grid, screen, cell_size, input_box, apply_button, input_text, font, steps_counter):
    selected_shape = "Pyramid"
    target_shape = PREDEFINED_SHAPES[selected_shape]
    dropdown_open = False
    global selected_topology, topology_dropdown_open
    limit_reached = False
    active_input = False

    draw_grid(screen, grid)
    draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text, selected_topology, topology_dropdown_open, steps_counter=steps_counter)
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

                # Handle Topology Dropdown Toggle
                if TOPOLOGY_DROPDOWN_X <= mx <= TOPOLOGY_DROPDOWN_X + TOPOLOGY_DROPDOWN_WIDTH and TOPOLOGY_DROPDOWN_Y <= my <= TOPOLOGY_DROPDOWN_Y + 30:
                    topology_dropdown_open = not topology_dropdown_open
                    event_occurred = True
                elif topology_dropdown_open:
                    for i, option in enumerate(topology_options):
                        if TOPOLOGY_DROPDOWN_Y + 30 * (i + 1) <= my <= TOPOLOGY_DROPDOWN_Y + 30 * (i + 2):
                            selected_topology = option
                            topology_dropdown_open = False
                            return ("TOPOLOGY", selected_topology.lower().replace(" ", "_"))


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
            draw_ui(screen, selected_shape, dropdown_open, input_box, apply_button, font, input_text, selected_topology, topology_dropdown_open, steps_counter=steps_counter)
            for row, col in target_shape:
                pygame.draw.rect(screen, (200, 100, 0),
                                 (col * cell_size, row * cell_size + HEADER_HEIGHT, cell_size, cell_size), 3)
            pygame.display.flip()
