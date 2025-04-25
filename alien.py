import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ss_game):
        """Initialize"""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("images/alien.png")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = 3 * self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact vertical position by float.
        # The defining of this variable is just for changing the speed by small
        # quantity. Without this variable, the speed only could be adjusted by
        # integer. Rect class only accept intergers.
        self.y = float(self.rect.y)

    def update(self):
        """Move the alien to the top or bottom."""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y
    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)