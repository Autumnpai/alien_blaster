from pathlib import Path
import pygame
class Gamestats:
    """Store the changing statistics in the horizonal game"""

    def __init__(self, hg_game):
        """Initialization"""
        self.settings = hg_game.settings
        self.reset_stats()
        # Read from highscore.txt, should never be reset.
        path = Path("highscore.txt")
        if not path.exists():
            self.high_score = 0
            path.write_text(str(self.high_score))
        else:
            self.high_score = int(path.read_text())
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.plane_left = self.settings.plane_limit
        self.score = 0
        self.level = 1