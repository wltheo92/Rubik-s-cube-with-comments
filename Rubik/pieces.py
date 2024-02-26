from typing import NewType, Dict, Literal

from colour import Colour

# Define how to move a piece so it's at a known location

# Define new type called Corner as dictionary with
# key - string
#       UFR - upper front right corner
#       DFR - lower front right corner
#       DBR - lower back right corner
#       URB - upper back right corner
#       ULF - upper front left corner
#       UBL - upper back left corner
#       DFL - lower front left corner
#       DBL - lower back left corner
# value - Colour
Corner = NewType("Corner", Dict[str, Colour])

# Define new type called Edge as dictionary with
# key - string
#       UF - upper front edge
#       UL - upper left edge
#       UR - upper right edge
#       UB - upper back edge
#       LB - back left edge
#       LD - lower left edge
#       LF - front left edge
#       RB - back right edge
#       RD - lower right edge
#       RF - front right edge
#       DB - lower back edge
#       DF - lower front edge
# value - Colour
Edge = NewType("Edge", Dict[str, Colour])

# Dictionary that defines the necessary moves to
# change a particular edge to upper front position
EDGE_TO_UF = {
    "UF": "U2 U2",  #To turn upper front edge to upper front position, make 2 half turns of upper face
    "UL": "U'",     #To turn upper left edge to upper front position, make a quarter turn of upper face in counter-clockwise direction
    "UR": "U",      #To turn upper right edge to upper front position, make a quarter turn of upper face in clockwise direction
    "UB": "U2",     #To turn upper back edge to upper front position, make a half turn of upper face
    "LB": "L2 F",   #To turn back left edge to upper front position, make a half turn of left face and a quarter turn of front face in clockwise direction
    "LD": "L' F",   #To turn lower left edge to upper front position, make a quarter turn of left face in counter-clockwise direction and a quarter turn of front face in clockwise direction
    "LF": "F",      #To turn front left edge to upper front position, make a quarter turn of front face in clockwise direction
    "RB": "R2 F'",  #To turn back right edge to upper front position, make a half turn of right face and a quarter turn of front face in counter-clockwise direction
    "RD": "R F'",   #To turn lower right edge to upper front position, make a quarter turn of right face in clockwise direction and a quarter turn of front face in counter-clockwise direction
    "RF": "F'",     #To turn front right edge to upper front position, make a quarter turn of front face in counter-clockwise direction
    "DB": "D2 F2",  #To turn lower back edge to upper front position, make a half turn of lower face and a half turn of right face
    "DF": "F2"      #To turn lower front edge to upper front position, make a half turn of front face
}

# Dictionary that defines the necessary moves to
# change a particular corner to upper front right position
CORNER_TO_UFR = {
    "UFR": "U2 U2", #To turn upper front right corner to upper front right position, make 2 half turns of upper face
    "DFR": "R",     #To turn lower front right corner to upper front right position, make a quarter turn of right face in clockwise direction
    "DBR": "R2",    #To turn lower back right corner to upper front right position, make a half turn of right faces
    "URB": "U",     #To turn upper back right corner to upper front right position, make a quarter turn of upper face in clockwise direction
    "ULF": "U'",    #To turn upper front left corner to upper front right position, make a quarter turn of upper face in counter-clockwise direction
    "UBL": "U2",    #To turn upper back left corner to upper front right position, make a half turn of upper face
    "DFL": "L' U'", #To turn lower front left corner to upper front right position, make a quarter turn of left face in counter-clockwise direction and a quarter turn of upper face in counter-clockwise direction
    "DBL": "L2 U'"  #To turn lower back left corner to upper front right position, make a half turn of left face and a quarter turn of upper face in counter-clockwise direction
}
