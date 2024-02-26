from typing import List, TypeVar, Union

from itertools import permutations

from move import Move
from colour import Colour, INITIAL_FACE_COLOUR_MAPPING
from pieces import Corner, Edge, CORNER_TO_UFR, EDGE_TO_UF
import parser
from generator import gen_scramble


# The model for the cube
class Cube:
    def __init__(self, size: int):
        # Define the size of rubik's cube
        self.size = size
        # Generate the initial faces as a dictionary with
        # key - face e.g. U(upper),D(lower),L(left),R(right),B(back),F(front)
        # value - 2d-array of colours (dimensions: self.size by self.size)
        # The default mapping is as follows:
        # U (upper face) - white
        # F (front face) - green
        # L (left face)  - orange
        # B (back face)  - blue
        # R (right face) - red
        # D (lower face) - yellow
        self.faces = {face: self._generate_face(colour, size) 
                      for face, colour in INITIAL_FACE_COLOUR_MAPPING}
        
    def reset(self):
        # Generates the initial faces (for details, refer to the previous part)
        self.faces = {face: self._generate_face(colour, self.size) 
                      for face, colour in INITIAL_FACE_COLOUR_MAPPING}
        
    def scramble(self):
        # Execute the moves of the generated scramble
        self.do_moves(gen_scramble())

    # Gets the value of a particular sticker
    def get_sticker(self, sticker: str) -> Colour:
        # Go through all the permutations (The dictionaries only store one permutation)
        for perm in permutations(sticker):
            # Find the edge in the dictionary and pass it to the appropriate function
            if "".join(perm) in EDGE_TO_UF:
                return self.get_edge("".join(perm))[sticker[0]]
            elif "".join(perm) in CORNER_TO_UFR:
                return self.get_corner("".join(perm))[sticker[0]]

        raise ValueError(f"Not a valid sticker: {sticker}")

    # Gets an edge piece, called with get_edge("UF") for the up-front edge piece
    def get_edge(self, piece: str) -> Edge:
        # Finds the moves needed to move that piece to a known location (up-front position)
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        # Do the moves and store the colour values into a dictionary indexed by the side names
        self.do_moves(moves)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })

        # Reverse the moves
        parser.invert_moves(moves)

        return info

    # Gets a corner piece
    def get_corner(self, piece: str) -> Corner:
        # Finds the moves needed to move that piece to a known location
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        # Do the moves and store the colour values into a dictionary indexed by the side names
        self.do_moves(moves)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })

        # Reverse the moves
        parser.invert_moves(moves)

        return info

    # Executes a sequence of moves
    def do_moves(self, moves: Union[str, List[Move]]):
        # If a string containing the moves was passed, convert it to a list of moves
        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        # Iterate through each move object in the moves list
        for move in moves:
            # Execute cube rotation when face attribute of move object is 'y'
            if move.face == "y":
                # Rotate the cube about the y-axis
                self._y_rotate()
            # Execute face rotation when face attribute of move object is 'U','D','F','B','L',or 'R'
            else:
                # Rotate an appropriate turn on appropriate face based on the attributes of move object
                self._rotate(move)

    # Checks if the cube is solved
    def is_solved(self) -> bool:
        # Go through each face and make sure all the colours on that face are the same
        # Iterate through each 2D-array of Colours
        for face in self.faces.values():
            # Iterate through each row of 2D-array
            for row in face:
                # If there is at least one Colour in the row that is not equal to the reference Colour in the first row and first column
                if any(piece_colour != face[0][0] for piece_colour in row):
                    # Output False since the cube is not solved
                    return False
        # Output True since the cube has been solved
        return True

    # Generates a 2d array of a single face
    # with the same numbers of rows and columns (determined by size)
    # populated by specified Colour objects
    def _generate_face(self, colour: Colour, size: int):
        return [[colour for _ in range(size)] for _ in range(size)]

    # Rotates a face
    # (1) reverse the order of nested list (2D-array)
    # (2) use zip to turn each column (from left to right) into a new row
    # (3) collect each new row in another list
    def _face_rotate(self, face: str):
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    # Rotates the adjacent faces to face, around the cube
    def _adjacent_face_swap(self, face: str):
        if face == "U":
            # List of faces to rotate
            l = [self.faces[face][0] for face in ["F", "L", "B", "R"]]

            # Rotate the faces
            self.faces["F"][0], self.faces["L"][0], \
                self.faces["B"][0], self.faces["R"][0] = l[-1:] + l[:-1]

        elif face == "D":
            # List of faces to rotate
            l = [self.faces[face][-1] for face in ["F", "L", "B", "R"]]

            # Rotate the faces
            self.faces["F"][-1], self.faces["L"][-1], \
                self.faces["B"][-1], self.faces["R"][-1] = l[1:] + l[:1]

        elif face == "F":
            # List of faces to rotate, transpose to change to local space of F
            l = [self.faces["U"], _transpose(self.faces["R"]),
                 self.faces["D"], _transpose(self.faces["L"])]
            
            # Rotate the faces
            r = [l[0][-1], l[1][0][::-1], l[2][0], l[3][-1][::-1]]

            l[0][-1], l[1][0], l[2][0], l[3][-1] = r[-1:] + r[:-1]

            # Store them back, undoing the transpose
            self.faces["U"][-1] = l[0][-1]
            self.faces["R"] = _transpose(l[1])
            self.faces["D"][0] = l[2][0]
            self.faces["L"] = _transpose(l[3])

        elif face == "R":
            # Thsi is the same as F, if we first rotate the cube
            self._y_rotate()
            self._adjacent_face_swap("F")
            self._y_rotate(inverse=True)

        elif face == "L":
            # Thsi is the same as F, if we first rotate the cube counter clockwise
            self._y_rotate(inverse=True)
            self._adjacent_face_swap("F")
            self._y_rotate()

        elif face == "B":
            # This is the same as F, if we first rotate the cube twice
            self._y_rotate(double=True)
            self._adjacent_face_swap("F")
            self._y_rotate(double=True)
            
    # Rotates a piece
    def _rotate(self, move: Move):
        # Simply calls the appropriate set of functions
        for _ in range(2 if move.double else 3 if move.invert else 1):
            self._face_rotate(move.face)
            self._adjacent_face_swap(move.face)

    # Rotates the entire cube about the y-axis
    def _y_rotate(self, double=False, inverse=False):
        for i in range(2 if double else 3 if inverse else 1):
            # Get the list of faces about the y axis
            l = [self.faces[face] for face in ["F", "L", "B", "R"]]
            # Swap them around
            self.faces["F"], self.faces["L"], self.faces["B"], self.faces["R"] = l[-1:] + l[:-1]

            # Rotate only the U and D layers to simulate the rest of the cubrs
            self._face_rotate("U")
            for _ in range(3):
                self._face_rotate("D")
    
# Helper function to transpsoe a face
T = TypeVar("T")
def _transpose(l: List[List[T]]) -> List[List[T]]:
    return [list(i) for i in zip(*l)]
