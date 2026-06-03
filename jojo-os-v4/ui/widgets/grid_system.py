GRID_SIZE = 50


def snap_to_grid(x, y):
    new_x = round(x / GRID_SIZE) * GRID_SIZE
    new_y = round(y / GRID_SIZE) * GRID_SIZE
    return new_x, new_y