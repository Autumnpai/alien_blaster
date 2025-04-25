import pygame

class Bullet(pygame.sprite.Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, h_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = h_game.screen
        self.settings = h_game.settings

        # Load the image of the bullet and set its rect attribute.
        self.image = pygame.image.load("images/missile.png")
        self.rect = self.image.get_rect()
        self.rect.midright = h_game.plane.rect.midright

        self.x = float(self.rect.x)
    
    def update(self):
        """Move the bullet to right of the screen"""
        # Update the exact position of the bullet.
        self.x += self.settings.bullet_speed
        self.rect.x = self.x