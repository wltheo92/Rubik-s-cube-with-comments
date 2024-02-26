from typing import List, Dict, Union

from cube import Cube
from pieces import Corner, Edge, EDGE_TO_UF, CORNER_TO_UFR
from move import Move
from colour import Colour
from collections import OrderedDict
import parser

# A cube that also keeps track of the history
class HistoryCube(Cube):
    def __init__(self, size: int, faces: Dict[str, List[List[Colour]]]=None):
        super().__init__(size)

        self.faces = faces if faces else self.faces
        self._history = []
        self._markers = []
        self._messages = []

    # Returns all the moves done on the cube
    def get_move_history(self) -> List[Move]:
        return self._history
    
    # Returns all the moves done on the cube, divided by sections
    def get_move_sections(self):
        # Current section
        current = []
        # Final return ditionary
        rvalue = OrderedDict()
        # Name of the current section
        msg = ""
        # Index of the last section
        lastMsgMarker = 0
        # Index of the last subsection
        lastMarker = 0
        first = True
        
        # Go through all the section names
        for marker, message in zip(self._markers, self._messages):
            # Initial setup
            if first:
                msg = message
                lastMsgMarker = marker
                first = False
                continue
            # Get the incoming subsection
            added = self._history[lastMarker:marker]

            # If there was a subsection, add it to the section
            if len(added) > 0: current.append(added)

            # If there is a new section
            if message != "":
                # Check if the section had any contents
                if current:
                    # Add it to the fina lreturn
                    i = 1
                    orig = msg
                    # Automatically add a number to the end if the section name already exists
                    while msg in rvalue:
                        msg = orig + f" {i}"
                        i += 1
                    rvalue[msg] = current

                # Reset the section data
                current = []
                # Keep track of the markers
                msg = message
                lastMsgMarker = marker
            lastMarker = marker
        # Clean the sections to make sure  there are no empty sections
        if len(current) > 0:
            i = 1
            orig = msg
            while msg in rvalue:
                msg = orig + f" {i}"
                i += 1
            rvalue[msg] = current
            rvalue[msg] = current
        current = []
        msg = message
        return rvalue
                

    # Starts a new section in the history
    def insertMarker(self, message):
        self._markers.append(len(self._history))
        self._messages.append(message)

    # Same as cube, except also keeps track of the moves
    def get_edge(self, piece: str) -> Edge:
        moves = parser.scramble_to_moves(EDGE_TO_UF[piece])

        self.do_moves(moves, False)
        info = Edge({
            piece[0]: Colour(self.faces["U"][-1][1]),
            piece[1]: Colour(self.faces["F"][0][1])
        })
        self.do_moves(parser.invert_moves(moves), False)

        return info

    # Same as cube, except also keeps track of the moves
    def get_corner(self, piece: str) -> Corner:
        moves = parser.scramble_to_moves(CORNER_TO_UFR[piece])

        self.do_moves(moves, False)
        info = Corner({
            piece[0]: Colour(self.faces["U"][-1][-1]), 
            piece[1]: Colour(self.faces["F"][0][-1]),
            piece[2]: Colour(self.faces["R"][0][0])
        })
        self.do_moves(parser.invert_moves(moves), False)

        return info

    # Same as cube, except also keeps track of the moves
    def do_moves(self, moves: Union[str, List[Move]], save_history: bool=True): 
        super().do_moves(moves)

        if isinstance(moves, str):
            moves = parser.scramble_to_moves(moves)

        if save_history:
            for move in moves:
                self._history.append(move)
