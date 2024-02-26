from typing import List

from copy import deepcopy

from cube import Cube
from move import Move
from colour import WHITE, YELLOW, GREEN, BLUE, ORANGE, RED
from history_cube import HistoryCube
from cleaner import clean_moves
from parser import scramble_to_moves, moves_to_scramble

# Generates a solution for the cube
def generate_solution(cube: Cube) -> List[Move]:
    cube_copy = HistoryCube(cube.size, deepcopy(cube.faces))

    if isSolved(cube):
        return {}

    if not crossIsSolved(cube_copy):
        cube_copy.insertMarker("Cross")
        solve_cross(cube_copy)
    
    if not cornersAreSolved(cube_copy):
        cube_copy.insertMarker("Corners")
        solve_corners(cube_copy)

    if not l2IsSolved(cube_copy):
        cube_copy.insertMarker("Second layer")
        solve_middle_edges(cube_copy)

    solve_eoll(cube_copy)
    solve_ocll(cube_copy)
    solve_cpll(cube_copy)
    solve_epll(cube_copy)
    solve_auf(cube_copy)

    # Get the move history from the cube
    moveSections = cube_copy.get_move_sections()
    returnDict = {}

    # Simplify each section
    for sectionName, moves in moveSections.items():
        returnDict[sectionName] = []
        for move in moves:
            returnDict[sectionName].append(scramble_to_moves(clean_moves(moves_to_scramble(move))))

    # Remove any empty sections after simplification
    toDelete = []
    for key in returnDict:
        returnDict[key] = [x for x in returnDict[key] if x != []]
        if len(returnDict[key]) == 0: toDelete.append(key)

    # Delete any empty sections
    for key in toDelete:
        del returnDict[key]
        
    return returnDict

#CHecks if the cube is solved
def isSolved(cube: HistoryCube):
    for f in ["U", "D", "L", "R", "F", "B"]:
        # Makes sure each face is the same
        downFace = cube.faces[f][0][0]
        for y in range(cube.size):
            for x in range(cube.size):
                if cube.faces[f][x][y] != downFace: 
                    return False
    return True

# Makes sure the cross is solved
def crossIsSolved(cube: HistoryCube):
    # a 2x2 has no cross
    if cube.size == 2: return True

    # Get the edge pieces
    p1 = cube.get_edge("DF")["D"] 
    p2 = cube.faces["D"][1][1]
    p3 = cube.get_edge("DB")["D"]
    p4 = cube.get_edge("LD")["D"]
    p5 = cube.get_edge("RD")["D"]

    # Make sure they're the same
    return p1 == p2 and p2 == p3 and p3 == p4 and p4 == p5

# Returns the adjacent faces of a face 
def complement(face):
    if face == "F" or face == "B": return ("R", "L")
    return ("F", "B")

# Checks if the corners are solved
def cornersAreSolved(cube: HistoryCube):
    downFace = cube.faces["D"][0][0]
    for y in range(cube.size):
        for x in range(cube.size):
            if cube.faces["D"][x][y] != downFace: 
                return False
            
    #for f in ["F", "B", "L", "R"]:
    #    c = complement(f)
    #    p1 = cube.get_sticker(f"{f}D{c[0]}")
    #    p2 = cube.get_sticker(f"{f}D{c[1]}")

    #    if p1 != p2: return False
    #    if cube.size != 2 and cube.get_edge(f"D{f}") != p1: return False

    return True

# Checks if the second layer is solved
def l2IsSolved(cube: HistoryCube):
    # A 2x2 has no second layer
    if cube.size == 2: return True

    # Go through each pair of edges
    for f in ["F", "B", "L", "R"]:
        # Check if they're the same
        c = complement(f)
        p1 = cube.get_sticker(f"{f}{c[0]}")
        p2 = cube.get_sticker(f"{f}{c[1]}")

        if p1 != p2: return False
        # MAke sure they're the same as the center
        if cube.faces[f][1][1] != p1: return False

    return True

# Generates a cross solution
def solve_cross(cube: HistoryCube):
    # Moves to solve edges depending on where they are
    EDGES = {
        "UF": "",
        "UL": "U'",
        "UR": "U",
        "UB": "U2",
        "LB": "L U' L'",
        "LD": "L2 U'",
        "LF": "L' U' L",
        "RB": "R' U R",
        "RD": "R2 U",
        "RF": "R U R'",
        "DB": "B2 U2",
        "DF": "F2"
    }

    # Go through each face and edge, first solve blue, then orange, etc.
    for colour in [BLUE, ORANGE, GREEN, RED]:
        for edge in EDGES:
            cur_edge = tuple(cube.get_edge(edge).values())

            # Check if its a edge to solve
            if cur_edge in [(colour, YELLOW), (YELLOW, colour)]:
                # Solve the edee
                cube.do_moves(EDGES[edge])

                # Insert into place (Either F2, or sledgehammer)
                if cube.get_edge("UF")["U"] == YELLOW:
                    cube.do_moves("F2")
                else:
                    cube.do_moves("R U' R' F")

                # Alignment
                cube.do_moves("D'")
                cube.insertMarker("")
                
                break

    cube.do_moves("D2")

# Generates a solution for the corner of a cube
def solve_corners(cube: Cube):
    CORNERS = {
        "UFR": "U2 U2",
        "DFR": "R U R' U'",
        "DBR": "R' U R U",
        "URB": "U",
        "ULF": "U'",
        "UBL": "U2",
        "DFL": "L' U' L",
        "DBL": "L U L' U" 
    }

    # Go through each target colour
    for colour1, colour2 in [(GREEN, RED), (BLUE, RED), 
                             (BLUE, ORANGE), (GREEN, ORANGE)]:
        for corner in CORNERS:
            cur_corner = cube.get_corner(corner).values()

            # Find and execute the correct solution to set up the corner
            if colour1 in cur_corner and colour2 in cur_corner and YELLOW in cur_corner:
                cube.do_moves(CORNERS[corner])

                # Solve the corner
                if cube.get_sticker("UFR") == YELLOW:
                    moves = "U R U2 R' U R U' R'"
                elif cube.get_sticker("FUR") == YELLOW:
                    moves = "U R U' R'"
                else:
                    moves = "R U R'"
                
                cube.do_moves(moves)
                cube.do_moves("D'")
                cube.insertMarker("")
                break
    
# SOlve layer 2
def solve_middle_edges(cube: Cube):
    EDGES = {
        "UF": "U2 U2",
        "UR": "U",
        "UL": "U'",
        "UB": "U2",
        "RF": "R' F R F' R U R' U'",
        "LF": "L F' L' F L' U' L U",
        "RB": "R' U R B' R B R'",
        "LB": "L U' L' B L' B' L"
    }
    # Go through each edge
    for colour1, colour2 in [(GREEN, RED), (RED, BLUE), (BLUE, ORANGE), (ORANGE, GREEN)]:
        for edge in EDGES:
            cur_edge = tuple(cube.get_edge(edge).values())

            # Match the edge to see if this is it
            if cur_edge == (colour1, colour2) or cur_edge == (colour2, colour1):
                # Set up the edge
                cube.do_moves(EDGES[edge])

                # Standard algorithm to insert edge
                if cube.get_sticker("FU") == colour1:
                    moves = "U R U' R' F R' F' R"
                else:
                    moves = "U2 R' F R F' R U R'"
                cube.do_moves(moves)
                cube.do_moves("y")
                cube.insertMarker("")

                break

# Solves the edge OL
def solve_eoll(cube: Cube):
    for _ in range(4):
        # Get te edge state
        top_layer = [cube.get_sticker("UB"), cube.get_sticker("UR"),
                     cube.get_sticker("UF"), cube.get_sticker("UL")]
        eo_state = [face == WHITE for face in top_layer]

        # Standard algorithm for different shapes
        if eo_state == [False, False, False, False]:
            cube.insertMarker("Dot OLL")
            cube.do_moves("R U2 R2 F R F' U2 R' F R F'")
            break
        elif eo_state == [False, False, True, True]:
            cube.insertMarker("Square OLL 1")
            cube.do_moves("U F U R U' R' F''")
            break
        elif eo_state == [False, True, False, True]:
            cube.insertMarker("Line OLL 1")
            cube.do_moves("F R U R' U' F'")
            break
        else:
            cube.do_moves("U")

# Solve complete OLL
def solve_ocll(cube: Cube):
    OCLLS = {
        "S": "R U R' U R U2 R' U",
        "AS": "U R' U' R U' R' U2 R",
        "H": "F R U R' U' R U R' U' R U R' U' F'",
        "Headlights": "R2 D' R U2 R' D R U2 R",
        "Sidebars": "U' L F R' F' L' F R F'",
        "Fish": "R' U2 R' D' R U2 R' D R2",
        "Pi": "U R U2 R2 U' R2 U' R2 U2 R"
    }

    def get_top_layer_corners(cube: Cube):
        return [cube.get_sticker("UBL"), cube.get_sticker("UBR"),
                cube.get_sticker("UFR"), cube.get_sticker("UFL")]

    def get_co_state(top_layer):
        return [face == WHITE for face in top_layer]

    cube.insertMarker("Alignment")
    for _ in range(4):
        # If the faces on the top are solved or not
        co_state = get_co_state(get_top_layer_corners(cube))

        # Checks for sdifferent setups and executes the correct algorithms in the dictionary
        if co_state == [False, False, False, False]:
            while cube.get_sticker("FUR") != WHITE or cube.get_sticker("FUL") != WHITE:
                cube.do_moves("U")

            if cube.get_corner("UFR")["F"] == cube.get_corner("UBL")["B"]: 
                cube.insertMarker("OLL (H)")
                cube.do_moves(OCLLS["H"])
            else:
                cube.insertMarker("OLL (PI)")
                cube.do_moves(OCLLS["Pi"])
            break
        elif co_state == [False, False, False, True]:
            if cube.get_sticker("FUR") == WHITE:
                cube.insertMarker("OLL (S)")
                cube.do_moves(OCLLS["S"])
            else:
                cube.insertMarker("OLL (AS)")
                cube.do_moves(OCLLS["AS"])
            break
        elif co_state == [False, False, True, True]:
            if cube.get_sticker("BRU") == WHITE:
                cube.insertMarker("OLL (Headlights)")
                cube.do_moves(OCLLS["Headlights"])
            else:
                cube.insertMarker("OLL (Sidebars)")
                cube.do_moves(OCLLS["Sidebars"])
            break
        elif co_state == [False, True, False, True]:
            cube.insertMarker("Fish")
            if cube.get_sticker("RUF") != WHITE:
                cube.do_moves("U2")
            cube.do_moves(OCLLS["Fish"])
            break
        else:
            cube.do_moves("U")


def solve_cpll(cube: Cube):
    # Standard algorithm to solve the corners 
    alg = "R' U L' U2 R U' R' U2 R L "

    cube.insertMarker("Alignment")
    for _ in range(4):
        # Nothing to be done, already solved
        if cube.get_sticker("FUR") == cube.get_sticker("FUL") and cube.get_sticker("BLU") == cube.get_sticker("BRU"):
            break
        
        if cube.get_sticker("FRU") == cube.get_sticker("FLU"):
            cube.insertMarker("PLL1")
            cube.do_moves(alg)
            break
        cube.do_moves("U")
    else:
        cube.insertMarker("PLL1")
        cube.do_moves(alg + " U " + alg)

# Final stage
def solve_epll(cube: Cube):
    solved_edges = 0

    cube.insertMarker("Alignment")
    for _ in range(4):
        if cube.get_sticker("FU") == cube.get_sticker("FUR"):
            solved_edges += 1
        cube.do_moves("U")

    if solved_edges != 4:
        if solved_edges == 0:
            cube.insertMarker("PLL (U)")
            cube.do_moves("R U' R U R U R U' R' U' R2")

        cube.insertMarker("Alignment")
        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.do_moves("U")

        cube.do_moves("U2")

        while cube.get_sticker("FU") != cube.get_sticker("FUR"):
            cube.insertMarker("PLL (U)")
            cube.do_moves("R U' R U R U R U' R' U' R2")

    cube.insertMarker("AUF")
    while cube.get_sticker("FU") != cube.get_sticker("FR"):
        cube.do_moves("U")

def solve_auf(cube: Cube):
    cube.insertMarker("AUF")
    while not cube.is_solved():
        cube.do_moves("U")
