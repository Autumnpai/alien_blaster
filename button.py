import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, hg_game, msg, text_color=(255, 255, 255)):
        """Initialize button attributes."""
        self.screen = hg_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (150, 200, 0)
        # self.text_color = (255, 255, 255)  # Default text color
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg, text_color)
    
    def _prep_msg(self, msg, text_color):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, text_color, 
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)