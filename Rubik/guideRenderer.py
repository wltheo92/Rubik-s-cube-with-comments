from button import *
import pygame
from solver import *

# A renderer for a calculated solution
# The renderer comprises of:
# (1) Toggle button to switch between Hide and Guide modes
# (2) Panel displaying the section and its corresponding solution
# (3) Solve Next button, which when clicked, executes the next move
class GuideRenderer:
        def __init__(self, x, y, cubeModel, moveCallback):
                # Set the x-coordinate of the top left corner of renderer
                self.x = x
                # Set the y-coordinate of the top left corner of renderer
                self.y = y
                # Assign the Cube object (used to generate solution and check if the cube is solved)
                self.cubeModel = cubeModel
                # Callback to use when moving the cube
                self.moveCallback = moveCallback

                # Buttons
                # Toggle button to switch between Guide and Hide modes
                self.toggle = Button(x, y, 100, 50, "Guide", self.enable, 'guide')
                # Solve Next button to execute the next move
                self.solveButton = Button(x, y+150, 140, 50, "Solve Next", self.solveNext, 'next')

                # Enable by default
                self.enable()

                # Set up the solution environment
                self.moves = None
                self.refreshSolution()

                # Incorrect moves count to know when to reset the solution
                self.incorrect = 0

        # Solves the next move
        def solveNext(self):
                # Retrive the next move
                move = self.nextMove()
                # If there is a move object (not None)
                if move:
                        # Execute the face rotation based on the attributes of move object
                        self.moveCallback(str(move))

        # Returns a list of event listeners to send events to
        def getListeners(self):
                return [self.toggle, self.solveButton]

        # Enables the renderer
        def enable(self):
                # Change the button
                # Convert the button text to "Hide"
                self.toggle.text = "Hide"
                # Change to enabled state, where the solution panel and Solve Next button are displayed when necessary
                self.enabled = True
                # Callback function triggered (to disable the renderer) when 'Hide' button is clicked
                self.toggle.action = self.disable
                # Name of image file of the button icon
                self.toggle.image_file = 'hide'
                # Upload the image file of the button icon
                self.toggle.image = pygame.image.load(f'images//{self.toggle.image_file}({self.toggle.suffix}).jpg')
                
                # Make sure the solution is up to date
                self.refreshSolution()

        def disable(self):
                # change the button
                # Convert the button text to "Guide"
                self.toggle.text = "Guide"
                # Change to disabled state, where the solution panel and Solve Next button are not displayed
                self.enabled = False
                # Callback function triggered (to enable the renderer) when 'Guide' button is clicked
                self.toggle.action = self.enable
                # Name of image file of the button icon
                self.toggle.image_file = 'guide'
                # Upload the image file of the button icon
                self.toggle.image = pygame.image.load(f'images//{self.toggle.image_file}({self.toggle.suffix}).jpg')

        # Retrieves the next move of the solution
        def nextMove(self):
                # By default have no key
                key = None
                # Just retrieve the first key in order
                for key in self.moves:
                        break
                # If there is no key, output None
                if key == None: return None
                # Get the first move of the next section
                return self.moves[key][0][0]
        
        # Adds a move in front of the move list
        def prependMove(self, move):
                # Retrieve the next move object
                nextMove = self.nextMove()

                # If there is no moves, create a new section called AUF
                if len(self.moves) == 0:
                        self.moves["auf"] = [[]]

                # Get the first key
                for key in self.moves:
                        break

                # Check if the new move can combine with the next move
                # If there is a next move object, and its face is identical to the face of the counter move object to be added,
                # then we don't add the counter move object but only modify the next move object
                if nextMove and nextMove.face == move.face:
                        # If the next move is a half turn, combined move is a quarter turn in the direction of added move
                        if nextMove.double:
                                # Turn the next move into a quarter turn
                                nextMove.double = False
                                # Set the direction of rotation to be the same as that of added move
                                nextMove.invert = move.invert
                        # if the next move is a quarter turn in the same direction as the added move, then a half turn is resulted
                        elif nextMove.invert == move.invert:
                                # Set the next move into a half turn
                                nextMove.double = True
                                nextMove.invert = False
                else:
                        # Prepend the move 
                        self.moves[key][0].insert(0, move)

        
        # Removes the next move from the solution
        def popNextMove(self):
                # Remove the next move
                for key in self.moves: break

                # Remove the first move
                self.moves[key][0] = self.moves[key][0][1:]

                # Check if the subsection is done, clear and move to the next subsection
                while len(self.moves[key]) != 0 and len(self.moves[key][0]) == 0:
                        self.moves[key] = self.moves[key][1:]

                # Check if the section is done, clear and move to the next section
                while key in self.moves and len(self.moves[key]) == 0:
                        del self.moves[key]
                        for key in self.moves: break

        # Gets a new solution from the solver
        def refreshSolution(self):
                self.moves = generate_solution(self.cubeModel)

        # Updates the current solution based on a move by the user
        def updateSolution(self, move):
                # Retrieve the next move
                nextMove = self.nextMove()

                # If it's an expected move, remove it
                if nextMove == move:
                        self.popNextMove()
                        return
                # If it's a move that is counter to the expected move, make it a double
                elif nextMove != None and nextMove.double and nextMove.face == move.face:
                        nextMove.double = False
                        nextMove.invert = move.invert
                else:
                        # If it's solved, we're done
                        if isSolved(self.cubeModel):
                                self.moves = {}
                                return
                        # If we make an incorrect move
                        if self.incorrect < 5:
                                # Keep track of how many incorect moves
                                self.incorrect += 1
                                # Invert the incoming move (so we can add the counter to the solution)
                                move.invert = not move.invert
                                # Add the counter move to the solution
                                self.prependMove(move)
                        else:
                                # If too many are wrong, just start over
                                self.refreshSolution()
                                self.incorrect = 0

        # Draws the renderer
        def draw(self, win):
                # Draw the Toggle (Guide/ Hide) button
                self.toggle.draw(win)

                # If the renderer is not enabled, do not display the solution panel and Solve Next button
                if not self.enabled: return
                
                # If it's solved, change the text to "solved"
                if len(self.moves) == 0:
                        key = "Solved"
                        value = ""
                else:
                        # Otherwise, populate the values with the next subsection
                        for key, value in self.moves.items():
                                value = value[0]
                                break
                        # Only draw the solve button if there is a next move
                        self.solveButton.draw(win)

                # Set the font type and size
                font = pygame.font.SysFont('Arial', 20)

                # Render section name
                text_surf = font.render(key, True, (0, 0, 0))
                win.blit(text_surf, (self.x+5, self.y+ self.toggle.height + 10))
                # Render the solution
                value = " ".join(map(str, value))
                # If the length of solution string does not exceed 25 characters, display
                # the solution in one line
                if len(value) <= 25:
                        text_surf = font.render(value, True, (0, 0, 0))
                        win.blit(text_surf, (self.x+5,
							 self.y + self.toggle.height + 35))
                # Otherwise display the solution string in two lines
                else:
                        end_no = 25
                        if value[24] != ' ' and value[25] != ' ': end_no = 24
                        text_surf1 = font.render(value[:end_no].strip(), True, (0, 0, 0))
                        text_surf2 = font.render(value[end_no:].strip(), True, (0, 0, 0))
                        win.blit(text_surf1, (self.x+5,
							 self.y + self.toggle.height + 35))
                        win.blit(text_surf2, (self.x+5,
							 self.y + self.toggle.height + 55))
                
                # Draw the border of the solution panel
                if value != '':
                        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x, self.y + self.toggle.height + 9, 203, 75), 2, 3)
