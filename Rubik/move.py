from dataclasses import dataclass

# Simple class to represent a rubiks cube move
@dataclass
class Move:
    # For Face Rotation: Face of Rubik's cube, can be U(upper),D(lower),F(front),B(back),L(left),R(right)
    # For Cube Rotation: only value is y (indicating the rotation of the cube about y-axis)
    face: str
    # If true, the direction of rotation is counter-clockwise
    # If false, the direction of rotation is clockwsie (by default)
    invert: bool
    # If true, a half turn is made
    # If false, a quarter turn is made
    double: bool

    # Generate string that represents the move
    # The string comprises of:
    # (1) Face rotation: the face of Rubik's cube to be turned, can be U,D,F,B,L,R
    #     Cube rotation: can only be y (rotating the cube about the y-axis)
    # (2) optional 2, which indicates a half-turn if present; a quarter turn is made if it is absent
    # (3) optional ', which indicates counter-clockwise direction if present; a clockwise direction is indicated if absent
    def __str__(self):
        return self.face + ("2" if self.double else ("'" if self.invert else ""))
