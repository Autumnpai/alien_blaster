import pygame
from pygame.sprite import Sprite

class Plane(Sprite):
    """A class to manage the plance"""

    def __init__(self, h_game):
        """Initialize"""
        super().__init__()
        self.screen = h_game.screen
        self.screen_rect = h_game.screen.get_rect()
        self.image = pygame.image.load("images/plane.png")
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft
        self.rect.x += 16 # make the plane moving to right a little.
        self.moving_up = False
        self.moving_down = False
        self.settings = h_game.settings

        # Store a float for the plane's vertical position, this variable is for
        # adjusting the speed of the plane by small quantity.
        self.y = float(self.rect.y)
    
    def update(self):
        """Update the plane's position based on the movement flag"""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.plane_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.plane_speed
        
        self.rect.y = self.y
    
    def blitme(self):
        """Draw the plane at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_plane(self):
        """make the plane back to initial place"""
        self.rect.midleft = self.screen_rect.midleft
        self.rect.x += 16 # make the plane moving to right a little.
        self.y = float(self.rect.y)
