from typing import List

import random

# Scramble generator

# Helper function to generate multiple scrambles
def gen_n_scrambles(n: int) -> List[str]:
    # Initialise a list to append generated scrambles
    scrambles = []

    # Generate and collect scrambles for n times
    for _ in range(n):
        scrambles.append(gen_scramble())

    # Output the list of n scrambles
    return scrambles

# Generates a scramble by randomly stringing together moves
def gen_scramble() -> str:
    # List of fundamental moves
    # U - quarter turn of top face clockwise
    # R - quarter turn of right face clockwise
    # L - quarter turn of left face clockwise
    # B - quarter turn of back face clockwise
    # D - quarter turn of bottom face clockwise
    # F - quarter turn of front face clockwise
    moves = ["U", "R", "L", "B", "D", "F"]

    # Initialise a list to collect randomly assigned moves
    scramble = []

    # Repeat the move assignement for 40 times
    for _ in range(40):
        # Generate random integer (0-2)
        rand_num = random.randint(0, 2)

        # If the random integer is 0
        if rand_num == 0:
            # Collect randomly selected fundamental move
            scramble.append(random.choice(moves))
        # If the random integer is 1
        elif rand_num == 1:
            # Collect randomly selected fundamental move but modified to half turn
            scramble.append(random.choice(moves) + "2")
        # If the random integer is 2
        else:
            # Collect randomly selected fundamental move but modified to counter-clockwise
            scramble.append(random.choice(moves) + "'")

    # Create a string with all assigned move notations (separated by single space)
    return " ".join(scramble)
