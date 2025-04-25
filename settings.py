class Settings:
    """ Store all settings for side shooter game."""

    def __init__(self):
        """Initialize the static settings"""
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (135, 206, 235)
        self.fullscreen = False

        # Bullet settings:
        self.bullet_height = 15
        self.bullet_width = 6
        self.bullet_color = (255, 64, 0)
        self.bullet_allowed = 3

        # Plane settings
        self.plane_limit = 3

        # How quickly the game speeds up and alien point values increase
        self.speedup_scale = 1.1
        self.score_scale = 1.1

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that changes"""
        self.bullet_speed = 2.0
        self.alien_speed = 0.75
        self.fleet_forward_speed = 15
        self.plane_speed = 1.2
        # fleet_direction of 1 represents down; -1 represents up.
        self.fleet_direction = -1
        # Score settings
        self.alien_points = 10
    
    def increase_speed(self):
        """increase speed settings and alien piont values."""
        self.plane_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_forward_speed *= 1.02
        self.alien_points = int(self.alien_points * self.score_scale)
    
