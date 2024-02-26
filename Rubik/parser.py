from typing import List, Tuple

from move import Move

# Converts a string of moves to a pythonic list of move objects
def scramble_to_moves(scramble: str) -> List[Move]:
    # Initialise a list to collect generated moves
    moves = []

    # Split the string into a list of moves and iterate through each move
    for move in scramble.split():
        # Detect if ' is present in move (if present, is_prime is True; otherwise is_prime is False)
        is_prime = "'" in move
        # Detect if 2 is present in move (if present, is_double is True; otherwise is_double is False)
        is_double = "2" in move
        # Generate Move instance with Rubik's cube face (for face rotation) or y (for cube rotation), Boolean indicating presence of ', and Boolean indicating the presence of 2,
        # and append Move instance in the moves list
        moves.append(Move(move[0], is_prime, is_double))

    # Output the list of moves
    return moves


# Converts a  list of move objects to string of moves
def moves_to_scramble(moves: List[Move]) -> str:
    # Initialise a list to collect string representing the notation of each move
    scramble = []

    # Iterate through each move in the moves list
    for move in moves:
        # Get the: (from the face attribute of move object)
        # (1) face of Rubik's cube to be rotated for face rotation, OR
        # (2) axis of rotation about which the cube is rotated
        cur_move = move.face

        # If the double attribute of move object is True (indicating that a half turn is made)
        if move.double:
            # Append 2 to the end of the notation string
            cur_move += "2"
        # If the inverst attribute of move object is True (indicating that a turn is made in counter-clockwise direction)
        elif move.invert:
            # Append ' to the end of the notation string
            cur_move += "'"

        # Collect the generated notation string in the scamble list
        scramble.append(cur_move)

    # Join all notations in the list as a string (separated by single spaces)
    return " ".join(scramble)

# Inverts a list of move so they counter the argument list
def invert_moves(moves: List[Move]):
    # Initialise a list to collect counter moves
    inverted_moves = []

    # Iterate through each move in the moves list in reversed order
    for move in reversed(moves):
        # Define a move object with the same face/ cube rotation but in opposite direction
        inverted_move = Move(move.face, not move.invert, move.double)
        # Collect the defined counter move in the list
        inverted_moves.append(inverted_move)

    # Output the list of counter moves
    return inverted_moves

# Code to test
'''
if __name__ == "__main__":
    scramble = "L U2 D B' R2 U2 F R B2 U2 R2 U R2 U2 F2 D R2 D F2"

    print(scramble_to_moves(scramble))
'''
