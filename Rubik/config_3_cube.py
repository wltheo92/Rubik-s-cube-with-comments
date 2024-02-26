
# Constants
# Width/ Height (in pixels) of APP window
WINDOW_SIZE = 800
# Angle of rotation (in radian) by which the cube rotates in each step
ROTATE_SPEED = 0.1
# Width of buttons
BUTTON_WIDTH = 100
# Height of buttons
BUTTON_HEIGHT = 50
# Space around each button
BUTTON_MARGIN = 20
# Width/ Height (in pixels) of each square in 2D net of Rubik's cube
CUBE_SIZE = 30
# Space between squares in 2D net of Rubik's cube
CUBE_GAP = 2
# Adjust 2D cube starting coordinates to place faces next to each other
CUBE_2D_START_X = (WINDOW_SIZE - (12 * CUBE_SIZE + 11 * CUBE_GAP)) // 2
CUBE_2D_Y_OFFSET = 150
CUBE_2D_START_Y = WINDOW_SIZE - (9 * CUBE_SIZE + 8 * CUBE_GAP) - CUBE_2D_Y_OFFSET
# Number of rows/ columns in each face of Rubik's cube
row_col = 3
#surface_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 0, 255)] (not used)
# Cube surfaces definition
cube_surfaces = [
    [0, 1, 2, 3],    # Front face
    [1, 5, 6, 2],    # Right face
    [5, 4, 7, 6],    # Back face
    [4, 0, 3, 7],    # Left face
    [4, 5, 1, 0],    # Bottom face
    [3, 2, 6, 7]     # Top face
]
