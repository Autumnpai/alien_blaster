import pygame.font
from pygame.sprite import Group

from plane import Plane

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, hg_game):
        """Initialize scorekeeping attributes."""
        self.hg_game = hg_game
        self.screen = hg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setttings = hg_game.settings
        self.stats = hg_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self._prep_images()
    
    def _prep_images(self):
        """Prepare all the images"""
        # Prepare the initial score image.
        self.prep_planes()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_image = pygame.transform.rotate(self.score_image, -90)

        # Display the score at the left bottom of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.midright = self.screen_rect.midright
        self.score_rect.x -= 10

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, 
                                    self.text_color, self.setttings.bg_color)
        self.high_score_image = pygame.transform.rotate(self.high_score_image, -90)
        
        # Center the high score on the right side of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.bottomright = self.screen_rect.bottomright
        self.high_score_rect.x -= 10
        self.high_score_rect.y -= 20

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = 10 + (76 / 2) * 3 # 76 is the height of plane.

    def show_score(self):
        """Draw scores, level, and planes vertically on the right side."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.planes.draw(self.screen)
    
    def prep_planes(self):
        """Show how many planes are left."""
        self.planes = Group()
        for plane_number in range(self.stats.plane_left):
            plane = Plane(self.hg_game)
            
            # Resize the plane's image by half
            plane.image = pygame.transform.scale(plane.image, 
            (plane.rect.width // 2, plane.rect.height // 2))
            plane.rect = plane.image.get_rect()
            
            # Position the plane
            plane.rect.x = self.screen_rect.right - plane.rect.width - 10
            plane.rect.y = 10 + plane_number * plane.rect.height
            self.planes.add(plane)