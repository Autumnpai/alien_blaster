import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to manage explosion effects."""

    def __init__(self, position, game, scale=1):
        """Initialize the explosion at a given position."""
        super().__init__()
        self.frames = []
        self._load_frames(scale)  # Pass scale to load frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)
        self.game = game
        self.frame_delay = 4  # Delay between frames
        self.frame_counter = 0

    def _load_frames(self, scale):
        """Load explosion animation frames and scale them."""
        """Load explosion animation frames from a sprite sheet and scale them."""
        sprite_sheet = pygame.image.load("images/explosion.png").convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width = sheet_width // 4  # Assuming 4 columns
        frame_height = sheet_height // 4  # Assuming 4 rows

        for row in range(4):  # 4 rows
            for col in range(4):  # 4 columns
                x = col * frame_width
                y = row * frame_height
                frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                if scale != 1:
                    frame = pygame.transform.scale(
                        frame, (frame.get_width() * scale, frame.get_height() * scale)
                    )
                self.frames.append(frame)
        """
        for i in range(1, 6):  # Assuming 5 frames named explosion1.png to explosion5.png
            frame = pygame.image.load(f"images/explosion-0{i}.png").convert_alpha()
            if scale != 1:
                frame = pygame.transform.scale(
                    frame, (frame.get_width() * scale, frame.get_height() * scale)
                )
            self.frames.append(frame)
        """

    def update(self):
        """Update the explosion animation."""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()  # Remove the explosion when animation is complete
