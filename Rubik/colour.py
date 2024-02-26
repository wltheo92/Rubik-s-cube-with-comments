from typing import NewType, Tuple

#Create a new type called Colour comprising of a tuple of 3 integers (0-255)
Colour = NewType("Colour", Tuple[int, int, int])

# Colour definitions based on RGB format
WHITE = Colour((255, 255, 255))
GREEN = Colour((0, 255, 0))
ORANGE = Colour((255, 165, 0))
YELLOW = Colour((255, 255, 0))
BLUE = Colour((0, 0, 255))
RED = Colour((255, 0, 0))
# List of 6 Defined Colours
colourList = [WHITE, GREEN, ORANGE, YELLOW, BLUE, RED]

# List of tuples that define the colours of all 6 faces of Rubik's cube
INITIAL_FACE_COLOUR_MAPPING = [("U", WHITE), ("F", GREEN), ("L", ORANGE), 
                               ("B", BLUE), ("R", RED), ("D", YELLOW)]
