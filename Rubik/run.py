#!/usr/bin/env python
# coding: utf-8
# In[ ]:
# In[ ]:
# # with row_col
# In[ ]:
import pygame
import cv2
from math import sin, cos, floor
from cube import *
from button import *
from guideRenderer import *
from colour import colourList

WINDOW_SIZE = 800
config_data = False
guideRenderer = None

# Draws surface
def draw_surface(indices, points, colors):
    surface_points = [points[i] for i in indices]
    # Iterates over 3
    for row in range(3):
        for col in range(3):
            # Gets the point at the current point, and send it to pygame
            p1 = get_point(surface_points, row, col)
            p2 = get_point(surface_points, row, col + 1)
            p3 = get_point(surface_points, row + 1, col + 1)
            p4 = get_point(surface_points, row + 1, col)
            pygame.draw.polygon(window, colors[row * 3 + col], [p1, p2, p3, p4])
            pygame.draw.polygon(window, (0, 0, 0), [p1, p2, p3, p4], 1)
            
# Retrieves the polygon points of the surface at row and column
def get_point(surface_points, row, col):
    # Use the retrieved surface points from the config to configure the points
    return (
        surface_points[0][0] + (surface_points[1][0] - surface_points[0][0]) * col / 3 +
        (surface_points[3][0] - surface_points[0][0]) * row / 3,
        surface_points[0][1] + (surface_points[1][1] - surface_points[0][1]) * col / 3 +
        (surface_points[3][1] - surface_points[0][1]) * row / 3
    )
# Calculates the normal fo a surface
def calculate_normal(surface, points):
    p1 = points[surface[0]]
    p2 = points[surface[1]]
    p3 = points[surface[2]]
    u = [p2[i] - p1[i] for i in range(3)]
    v = [p3[i] - p1[i] for i in range(3)]
    normal = [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
    return normal

# Checks of a normal is facing the camera
def is_facing_camera(normal):
    return normal[2] > 0

# Matrix multiplication
def multiply_m(a, b):
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print('INCOMPATIBLE MATRIX SIZES')
    return product

# Class to render 2d cube representation
class SquareButton:
    def __init__(self, x, y, size, face, index):
        self.x = x
        self.y = y
        self.size = size
        self.face = face
        self.index = index
        self.accent_color = (0,0,0)

    # Sets the accent colour if it's being moused over
    def mouse_over(self, pos):
        y = self.index // cubeModel.size
        x = self.index % cubeModel.size

        # Return if center piece
        if cubeModel.size %2 == 1 and y == cubeModel.size // 2 and x == cubeModel.size // 2: return 

        if self.is_over(pos):
            self.accent_color = (-25, -25, -25)
        else:
            self.accent_color = (0, 0, 0)

    def draw(self, win):
        # Get the current colour of the cube
        current_color = list(colors[self.face][self.index])
        
        # Accent the colour, clamping to possible colour values
        for i in range(3):
            current_color[i] += self.accent_color[i]
            current_color[i] = min(max(0, current_color[i]), 255)

        # Draw the button
        pygame.draw.rect(win, current_color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.size, self.size), 1)

    # Checks if a position is in a button
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.size and self.y < pos[1] < self.y + self.size:
            return True
        return False
    
    # Cycles the colour of the button
    def cycle_color(self, cubeModel):
        # Cycle through the surface_colors list
        modelFace = view_index_to_model_index(self.face)
        y = self.index // cubeModel.size
        x = self.index % cubeModel.size

        # Return if center piece
        if cubeModel.size %2 == 1 and y == cubeModel.size // 2 and x == cubeModel.size // 2: return 

        currentIndex = colourList.index(cubeModel.faces[modelFace][y][x])
        cubeModel.faces[modelFace][y][x] \
            = colourList[(currentIndex+1) % len(colourList)]
        translate_model(cubeModel)

############################### ############## ###################################################### ################## $
def draw_surface(indices, points, colors, row_col):
    surface_points = [points[i] for i in indices]
    for row in range(row_col):
        for col in range(row_col):
            p1 = get_point(surface_points, row, col)
            p2 = get_point(surface_points, row, col + 1)
            p3 = get_point(surface_points, row + 1, col + 1)
            p4 = get_point(surface_points, row + 1, col)
            pygame.draw.polygon(window, colors[row * row_col + col], [p1, p2, p3, p4])
            pygame.draw.polygon(window, (0, 0, 0), [p1, p2, p3, p4], 1)
def get_point(surface_points, row, col):
    return (
        surface_points[0][0] + (surface_points[1][0] - surface_points[0][0]) * col / row_col +
        (surface_points[3][0] - surface_points[0][0]) * row / row_col,
        surface_points[0][1] + (surface_points[1][1] - surface_points[0][1]) * col / row_col +
        (surface_points[3][1] - surface_points[0][1]) * row / row_col
    )
def calculate_normal(surface, points):
    p1 = points[surface[0]]
    p2 = points[surface[1]]
    p3 = points[surface[2]]
    u = [p2[i] - p1[i] for i in range(3)]
    v = [p3[i] - p1[i] for i in range(3)]
    normal = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    return normal
def is_facing_camera(normal):
    return normal[2] > 0
def multiply_m(a, b):
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print('INCOMPATIBLE MATRIX SIZES')
    return product
def draw_2d_cube(square_buttons):
    for button in square_buttons:
        button.draw(window)
def change_color(new_color):
    global colors
    colors = [[new_color] * 9 for _ in range(6)]

# Buttons for color change
# Rotate functions
def rotate_x_pos():
    global angle_x
    angle_x += ROTATE_SPEED
def rotate_x_neg():
    global angle_x
    angle_x -= ROTATE_SPEED
def rotate_y_pos():
    global angle_y
    angle_y += ROTATE_SPEED
def rotate_y_neg():
    global angle_y
    angle_y -= ROTATE_SPEED
def rotate_z_pos():
    global angle_z
    angle_z += ROTATE_SPEED
def rotate_z_neg():
    global angle_z
    angle_z -= ROTATE_SPEED

def Create_square_buttons_for_the_2D_representation(row_col):
    # Create square buttons for the 2D representation
    # Create square buttons for 2D representation
    square_buttons = []
    if row_col == 3:
        for i in range(6):
            for j in range(9):
                face = i
                row = j // 3
                col = j % 3
                if face == 0:  # Front face
                    x = CUBE_2D_START_X + (3 + col) * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + (3 + row) * (CUBE_SIZE + CUBE_GAP)
                elif face == 1:  # Right face
                    x = CUBE_2D_START_X + (6 + col) * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + (3 + row) * (CUBE_SIZE + CUBE_GAP)
                elif face == 2:  # Back face
                    x = CUBE_2D_START_X + (9 + col) * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + (3 + row) * (CUBE_SIZE + CUBE_GAP)
                elif face == 3:  # Left face
                    x = CUBE_2D_START_X + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + (3 + row) * (CUBE_SIZE + CUBE_GAP)
                elif face == 4:  # Bottom face
                    x = CUBE_2D_START_X + (3 + col) * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 5:  # Top face
                    x = CUBE_2D_START_X + (3 + col) * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + (6 + row) * (CUBE_SIZE + CUBE_GAP)
                square_buttons.append(SquareButton(x, y, CUBE_SIZE, face, j))
    elif row_col == 2:
        for i in range(6):
            for j in range(4):  # Adjusted for 2x2 cube
                face = i
                row = j // 2
                col = j % 2
                if face == 0:  # Front face
                    x = CUBE_2D_START_X + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 1:  # Right face
                    x = CUBE_2D_START_X + 2 * (CUBE_SIZE + CUBE_GAP) + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 2:  # Back face
                    x = CUBE_2D_START_X + 4 * (CUBE_SIZE + CUBE_GAP) + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 3:  # Left face
                    x = CUBE_2D_START_X - 2 * (CUBE_SIZE + CUBE_GAP) + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 4:  # Bottom face
                    x = CUBE_2D_START_X + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y - 2 * (CUBE_SIZE + CUBE_GAP) + row * (CUBE_SIZE + CUBE_GAP)
                elif face == 5:  # Top face
                    x = CUBE_2D_START_X + col * (CUBE_SIZE + CUBE_GAP)
                    y = CUBE_2D_START_Y + 2 * (CUBE_SIZE + CUBE_GAP) + row * (CUBE_SIZE + CUBE_GAP)
                square_buttons.append(SquareButton(x, y, CUBE_SIZE, face, j))
    return square_buttons

#################################################################
#  MODEL TRANSLATIONS                                           #
#################################################################
# This was needed since the viewmodel was very different from the model
# Given a model index, return the corresponding view index
def model_face_to_view_index(face):
    if face == "F":
        return 0
    elif face == "B":
        return 2
    elif face == "L":
        return 3
    elif face == "R":
        return 1
    elif face == "U":
        return 4
    elif face == "D":
        return 5
    
# Reverse of above
def view_index_to_model_index(face):
    if face == 0:
        return "F"
    elif face == 2:
        return "B"
    elif face == 3:
        return "L"
    elif face == 1:
        return "R"
    elif face == 4:
        return "U"
    elif face == 5:
        return "D"

    
# Returns the mapping between the view indicies and model indicies
def view_model_mapping(face):
    uniform = [0,1,2, 3,4,5, 6,7,8]
    return uniform # The current model has no mapping, just return identity
    
# Convert 1d to 2d index
def dTo2D(index, cube):
    return (floor(index / cube.size), index % cube.size)

# Translates the model into the viewmodel
def translate_model(cube):
        for face_num, face in enumerate(["U", "F", "D", "B", "L", "R"]):
            face_num = model_face_to_view_index(face)
            for row_num, row in enumerate(cube.faces[face]):
                for cubie_num, cubie in enumerate(row):
                    colors[face_num][row_num*cube.size+cubie_num] = cubie

# Rotates a face
def rotateFace(face):
    # Checks if it's prime
    prime = len(face) == 2 and face[1] == "'"
    # Remove all decorators (2 or ')
    face = face[0]
    print(face)

    # Construct a move object (it can never be double)
    move = Move(face, prime, False)
    # DO the moves
    cubeModel.do_moves([move])
    move_soundfx.play()
    # Update the view model
    translate_model(cubeModel)

    guideRenderer.updateSolution(move)


# Define surface colors
#
# Pygame initialization
########################################### importnats
current_window = 0
def change_current_window():
    pass
# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()
move_soundfx = pygame.mixer.Sound("sounds//rubik.mp3")
button_soundfx = pygame.mixer.Sound("sounds//button.mp3")

# Initialize video
video = cv2.VideoCapture("images\\rubik.mp4")
success, video_image = video.read()
# Get FPS of video
fps = video.get(cv2.CAP_PROP_FPS)

# Core loop
while True:
    # set framerate
    clock.tick(fps)
    # Backgroudn colour
    window.fill((255, 255, 255))
    config_data = False
    if current_window == 0: ##main menu
        video_I = 0
        ################################## creat option button 1
        option_buttons = []
        button_x = 20
        button_y = 455
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 50
        name = '3 cube'
        image_file = '3-rubric'
        option_buttons.append(Button(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, name, change_current_window(),image_file))
        #################################
        ################################## creat option button 2
        #option_buttons = []
        button_x = 20
        button_y = 510
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 50
        name = '2 cube'
        image_file = '2-rubric'
        option_buttons.append(Button(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, name, change_current_window(),image_file))
        #################################
        while current_window == 0:
            ######################## video loop
            # Update the video image with proper timing
            if video_I < fps:
                video_I += 3
            else:
                success, video_image = video.read()
                video_I = 0
            if success:
                video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                video = cv2.VideoCapture("images\\rubik.mp4")
            # Display the video
            window.blit(video_surf, (0, 0))
            # Draw a blue-coloured rectangle to block the watermark of video
            pygame.draw.rect(window, (36, 147, 247), pygame.Rect(578,388,255,51))
            # Draw the title of APP
            window.blit(pygame.image.load('images\\title.jpg'),(5,150))
            ######################## buttons loop
            for button in option_buttons:
                button.draw(window)
            ########################
            # Event handling and key inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for button in option_buttons:
                        button.mouse_over(pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in option_buttons:
                        if button.is_over(pos):
                            button_soundfx.play()
                            if button.text == '3 cube':
                                current_window = 1
                                print(current_window)
                                #break
                            elif button.text == '2 cube':
                                current_window = 2
                                print(current_window)
                                #break
            pygame.display.update()
    ################################################################################################################################
    else:
        # Set initial colors for each face
        colors = [[(255,255,255) for _ in range(9)] for i in range(6)]

        # Creates the model
        cubeModel = Cube(2 if current_window == 2 else 3)
        translate_model(cubeModel)

        # Callback functions for the buttons
        def scramble():
            cubeModel.scramble()
            guideRenderer.refreshSolution()

        def reset():
            cubeModel.reset()
            guideRenderer.refreshSolution()

        if current_window == 1: # 1 means 3x3x3
            if config_data == False: # initialization for 6x6
                from config_3_cube import *
                config_data = True
                extra_buttons = []

                # Create the guide renderer
                guideRenderer = GuideRenderer(BUTTON_MARGIN, BUTTON_MARGIN + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN), cubeModel, rotateFace)

                # Scramble button
                button_x = BUTTON_MARGIN
                button_y = BUTTON_MARGIN + 1 * (BUTTON_HEIGHT + BUTTON_MARGIN)
                extra_buttons.append(Button(button_x, button_y, 130, BUTTON_HEIGHT, "Scramble", scramble,'scramble'))
                translate_model(cubeModel)

                button_x = BUTTON_MARGIN
                button_y = BUTTON_MARGIN + 0 * (BUTTON_HEIGHT + BUTTON_MARGIN)
                extra_buttons.append(Button(button_x, button_y, 130, BUTTON_HEIGHT, "Reset", reset,'reset'))
                
                # Buttons to rotate the cube
                extra_buttons.append(Button(176, 460, 30, 30, None, lambda: rotateFace("B'"), 'left'))
                extra_buttons.append(Button(594, 460, 30, 30, None, lambda: rotateFace("B"), 'right'))
                extra_buttons.append(Button(176, 524, 30, 30, None, lambda: rotateFace("F"), 'left'))
                extra_buttons.append(Button(594, 524, 30, 30, None, lambda: rotateFace("F'"), 'right'))
                extra_buttons.append(Button(305, 331, 30, 30, None, lambda: rotateFace("L"), 'up'))
                extra_buttons.append(Button(369, 331, 30, 30, None, lambda: rotateFace("R"), 'up'))
                extra_buttons.append(Button(401, 427, 30, 30, None, lambda: rotateFace("U"), 'up'))
                extra_buttons.append(Button(465, 427, 30, 30, None, lambda: rotateFace("D'"), 'up'))
                extra_buttons.append(Button(305, 653, 30, 30, None, lambda: rotateFace("L'"), 'down'))
                extra_buttons.append(Button(369, 653, 30, 30, None, lambda: rotateFace("R'"), 'down'))
                extra_buttons.append(Button(401, 557, 30, 30, None, lambda: rotateFace("U'"), 'down'))
                extra_buttons.append(Button(465, 557, 30, 30, None, lambda: rotateFace("D"), 'down'))

        if current_window == 2: # 2 means 2x2x2
            if config_data == False: # initialization for 6x6
                from config_2_cube import *
                config_data = True
                extra_buttons = []

                # Scramble button
                button_x = BUTTON_MARGIN
                button_y = BUTTON_MARGIN + 1 * (BUTTON_HEIGHT + BUTTON_MARGIN)
                extra_buttons.append(Button(button_x, button_y, 130, BUTTON_HEIGHT, "Scramble", scramble, 'scramble'))
                translate_model(cubeModel)

                button_x = BUTTON_MARGIN
                button_y = BUTTON_MARGIN + 0 * (BUTTON_HEIGHT + BUTTON_MARGIN)
                extra_buttons.append(Button(button_x, button_y, 130, BUTTON_HEIGHT, "Reset", reset, 'reset'))

                guideRenderer = GuideRenderer(BUTTON_MARGIN, BUTTON_MARGIN + 2 * (BUTTON_HEIGHT + BUTTON_MARGIN), cubeModel, rotateFace)

                # Buttons to rotate the cube
                extra_buttons.append(Button(168, 487, 40, 40, None, lambda: rotateFace("U"), 'left'))
                extra_buttons.append(Button(588, 487, 40, 40, None, lambda: rotateFace("U'"), 'right'))
                extra_buttons.append(Button(168, 534, 40, 40, None, lambda: rotateFace("D'"), 'left'))
                extra_buttons.append(Button(588, 534, 40, 40, None, lambda: rotateFace("D"), 'right'))
                
                extra_buttons.append(Button(356, 348, 40, 40, None, lambda: rotateFace("R'"), 'up'))
                extra_buttons.append(Button(356, 673, 40, 40, None, lambda: rotateFace("R"), 'down'))
                
                extra_buttons.append(Button(401, 439, 40, 40, None, lambda: rotateFace("F"), 'up'))
                extra_buttons.append(Button(401, 581, 40, 40, None, lambda: rotateFace("F'"), 'down'))
                extra_buttons.append(Button(448, 439, 40, 40, None, lambda: rotateFace("B"), 'up'))
                extra_buttons.append(Button(448, 581, 40, 40, None, lambda: rotateFace("B'"), 'down'))
                
                extra_buttons.append(Button(309, 673, 40, 40, None, lambda: rotateFace("L'"), 'down'))
                extra_buttons.append(Button(309, 348, 40, 40, None, lambda: rotateFace("L"), 'up'))


        #########################################################################################################################
        ###################### manually creating the back button
        button_x = 650
        button_y = 20
        BUTTON_WIDTH_temp = 110
        BUTTON_HEIGHT_temp = 50
        name = 'BACK'
        extra_buttons.append(Button(button_x, button_y, BUTTON_WIDTH_temp, BUTTON_HEIGHT_temp, name, change_current_window(),'back'))
        ###################### 2cube controls
        ####################### =623
        projection_matrix = [[1,0,0],
                             [0,1,0],
                             [0,0,0]]
        # Cube points
        cube_points = [
            [[-1], [-1], [1]],
            [[1], [-1], [1]],
            [[1], [1], [1]],
            [[-1], [1], [1]],
            [[-1], [-1], [-1]],
            [[1], [-1], [-1]],
            [[1], [1], [-1]],
            [[-1], [1], [-1]]
        ]
        # Main loop
        scale = 100
        angle_x = angle_y = angle_z = 0

        # Rotate buttons
        rotate_buttons = [
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 0, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot X+', rotate_x_pos, 'rotate_x_ac'),
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 1, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot X-', rotate_x_neg, 'rotate_x_c'),
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 2, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot Y+', rotate_y_pos, 'rotate_y_ac'),
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 3, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot Y-', rotate_y_neg, 'rotate_y_c'),
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 4, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot Z+', rotate_z_neg, 'rotate_z_ac'),
            Button(BUTTON_MARGIN + (BUTTON_WIDTH + BUTTON_MARGIN) * 5, WINDOW_SIZE - BUTTON_HEIGHT - BUTTON_MARGIN, 110, BUTTON_HEIGHT, 'Rot Z-', rotate_z_pos, 'rotate_z_c')
        ]
        # Create square buttons for the 2D representation
        square_buttons = Create_square_buttons_for_the_2D_representation(row_col)
        buttons = extra_buttons + rotate_buttons 
        event_buttons = extra_buttons + rotate_buttons + guideRenderer.getListeners() 

        while current_window == 1 or current_window == 2:
            clock.tick(60)
            window.fill((255, 255, 255))

            # Rotation matrices
            rotation_x = [[1, 0, 0],
                          [0, cos(angle_x), -sin(angle_x)],
                          [0, sin(angle_x), cos(angle_x)]]
            rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                          [0, 1, 0],
                          [-sin(angle_y), 0, cos(angle_y)]]
            rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                          [sin(angle_z), cos(angle_z), 0],
                          [0, 0, 1]]
            # Transform and project points
            points = [0 for _ in range(len(cube_points))]
            points_3d = [0 for _ in range(len(cube_points))]
            i = 0
            for point in cube_points:
                rotated = multiply_m(rotation_x, point)
                rotated = multiply_m(rotation_y, rotated)
                rotated = multiply_m(rotation_z, rotated)
                points_3d[i] = [rotated[0][0], rotated[1][0], rotated[2][0]]
                projected = multiply_m(projection_matrix, rotated)
                x = (projected[0][0] * scale) + (WINDOW_SIZE / 2)
                y = (projected[1][0] * scale) + (WINDOW_SIZE / 4)
                points[i] = (x, y)
                i += 1
            # Draw surfaces
            for i, surface in enumerate(cube_surfaces):
                normal = calculate_normal(surface, points_3d)
                if is_facing_camera(normal):
                    draw_surface(surface, points, colors[i], row_col)
            # Draw 2D unfolded cube representation with buttons
            draw_2d_cube(square_buttons)
            # Draw buttons
            for button in buttons:
                button.draw(window)
            # Draw guide
            guideRenderer.draw(window)
            # Event handling and key inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Mouse moved
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    # Send to buttons for hover effect
                    for button in event_buttons:
                        button.mouse_over(pos)
                    for square_button in square_buttons:
                        square_button.mouse_over(pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Send to button for actions
                    for button in event_buttons:
                        if button.is_over(pos):
                            button_soundfx.play()
                            # Special case if it's the back button
                            if button.text == 'BACK':
                                current_window = 0
                            else:
                                button.action()
                            translate_model(cubeModel)
                    for square_button in square_buttons:
                        if square_button.is_over(pos):
                            square_button.cycle_color(cubeModel)
                            guideRenderer.disable()
                # Handle key down
                elif event.type == pygame.KEYDOWN:
                    # Rotation is prime if shift is held down
                    prime = pygame.key.get_pressed()[pygame.K_LSHIFT]
                    key = pygame.key.name(event.key)

                    # Face rotations
                    if key in {"u", "f", "l", "r", "d", "b"}:
                        rotateFace(key.upper() + ("'" if prime else ""))
                    # Cube rotation
                    if key == "y":
                        rotateFace("y" + ("'" if prime else ""))
                        angle_y += 90
            # handle view rotations
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                angle_y += ROTATE_SPEED
            if keys[pygame.K_RIGHT]:
                angle_y -= ROTATE_SPEED
            if keys[pygame.K_UP]:
                angle_x += ROTATE_SPEED
            if keys[pygame.K_DOWN]:
                angle_x -= ROTATE_SPEED
            if keys[pygame.K_q]:
                angle_z -= ROTATE_SPEED
            if keys[pygame.K_e]:
                angle_z += ROTATE_SPEED
            # Update display
            pygame.display.update()
    pygame.display.update()
# In[ ]:
# In[ ]:
# In[ ]:
