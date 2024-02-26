
import pygame
###############
# Button class
class Button:
    # Initialize button instance
    def __init__(self, x, y, width, height, text, action, image_file):
        # x-coordinate of top left of button
        self.x = x
        # y-coordinate of top left of button
        self.y = y
        # width of button
        self.width = width
        # height of button
        self.height = height
        # text to be written over the button
        self.text = text
        # function called when button is clicked
        self.action = action
        # non-hover state colour of button
        self.colourAccent = (180, 180, 180)
        # name of image file of the button icon
        self.image_file = image_file
        # variable representing the state of button, i.e. 1 (not hovered), 2 (hovered)
        self.suffix = 1
        # loading image of icon
        self.image = pygame.image.load(f'images//{self.image_file}({self.suffix}).jpg')

    # Mouse over event handler
    def mouse_over(self, pos):
        # Change the colour of button depending on hover state
        # Triggered when button is hovered
        if self.is_over(pos):
            # Change to hover state colour
            self.colourAccent = (150, 150, 150)
            # Change button state to hover state
            self.suffix = 2
        # Triggered when button is not hovered
        else:
            # Change to non-hover state colour
            self.colourAccent = (180, 180, 180)
            # Change button state to non-hover state
            self.suffix = 1
        # loading image of icon corresponding to the button state
        self.image = pygame.image.load(f'images//{self.image_file}({self.suffix}).jpg')

    def draw(self, win):
        # Rendering the button on the canvas
        # Draw the shadow of button
        pygame.draw.rect(win, (100, 100, 100, 10), pygame.Rect(self.x+2, self.y+2, self.width, self.height),0,5)
        # Draw the button
        pygame.draw.rect(win, self.colourAccent, pygame.Rect(self.x, self.y, self.width, self.height),0,5)
        # Draw the border of button
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height), 2, 5)
        # Specify the font type and size
        font = pygame.font.SysFont('Arial', 20)
        # Triggered when the button has a text over it
        if self.text:
            # Create the button text
            text_surf = font.render(self.text, True, (0, 0, 0))
            # Paste the icon on the button
            win.blit(self.image, (self.x+5, self.y+5))
            # Paste the text over the button
            win.blit(text_surf, (self.x + 40 + (self.width - 45 - text_surf.get_width()) // 2,
                             self.y + (self.height - text_surf.get_height()) // 2))
        # Triggered when the button does not have a text over it
        else:
            # Paste the icon on the button (centered)
            win.blit(self.image, (self.x + (self.width - self.image.get_width()) // 2,
                            self.y + (self.height - self.image.get_height()) // 2))

    # Checks whether the button is hovered
    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
