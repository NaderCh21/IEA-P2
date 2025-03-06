# shape_selector.py
import pygame
from draw import draw_grid

def get_cell_under_mouse(pos, cell_size):
    """Returns the (row, col) of the grid cell under the mouse cursor."""
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return row, col

def select_target_shape(grid, screen, cell_size):
    """
    Allows the user to define a target shape by clicking on grid cells.
    Press ENTER to finalize the shape.
    Returns a list of (row, col) coordinates representing the target shape.
    """
    target_shape = []
    selecting = True

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Click to select shape cells
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_cell_under_mouse(pygame.mouse.get_pos(), cell_size)
                if (row, col) not in target_shape:
                    target_shape.append((row, col))

            # Press ENTER to confirm selection
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                selecting = False

        # Display the current selection
        draw_grid(screen, grid)
        for row, col in target_shape:
            pygame.draw.rect(screen, (200, 100, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 3)
        pygame.display.flip()

    return target_shape
