import sys
from time import sleep
from pathlib import Path

import pygame
import pygame.mixer  # Add mixer for sound effects

from settings import Settings
from plane import Plane
from bullet import Bullet
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard
from explosion import Explosion  # Import the Explosion class

class Horizongame:
    """Overall class to manage game assets and behaviors"""
    
    def __init__(self):
        """Initialize"""
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for sound effects
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.stats = Gamestats(self)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Blaster")

        # Load sound effects
        self.bullet_sound = pygame.mixer.Sound("sounds/bullet.wav")
        self.alien_hit_sound = pygame.mixer.Sound("sounds/explode.wav")

        # Load and play background music
        pygame.mixer.music.load("sounds/War2.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop indefinitely

        # Create the main essets
        self.plane = Plane(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()  # Group to manage explosions
        self._create_fleet()
        self._create_buttons()
        self.sb = Scoreboard(self)

        self.game_active = False
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._events_check()
            if self.game_active:
                self.plane.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60) # this changes the speed of the game, 
                                # not only the screen refresh rate. 
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.bullets.draw(self.screen)
        self.plane.blitme()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)  # Draw explosions

        # Draw the score information.
        self.sb.show_score()

        # Draw the start buttion if the game is inactive.
        if not self.game_active:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.hell_button.draw_button()
            self.quit_button.draw_button()
            self.wf_button.draw_button()
            pygame.mouse.set_visible(True)
        
        if self.game_active:
            pygame.mouse.set_visible(False)

        pygame.display.flip()
    
    def _events_check(self):
        """Response to the keypresses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.plane.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.plane.moving_down = True
                if event.key == pygame.K_q:
                    self._save_exit()
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
                if event.key == pygame.K_ESCAPE:
                    self.game_active = not self.game_active
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.plane.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.plane.moving_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()  # Play bullet firing sound

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets."""
        # Update bullet's positions.
        self.bullets.update()
        # Get rid of the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        self.explosions.update()  # Update explosions

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit the aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, 
                                                True, True)
        if collisions:
            for bullet, aliens in collisions.items():
                for alien in aliens:
                    # Calculate the exact collision point
                    collision_point = (bullet.rect.centerx, alien.rect.centery)
                    explosion = Explosion(collision_point, self)
                    self.explosions.add(explosion)
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.alien_hit_sound.play()  # Play alien hit sound

        if not self.aliens:
            while self.explosions:
                self._update_screen()
                self.explosions.update()
                self.alien_hit_sound.play()
                self.clock.tick(60)
            sleep(2.5)
            self._start_new_level()
    
    def _start_new_level(self):
        """reset the screen and start a new level after destroyed all aliens."""
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all 
        aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        collision = pygame.sprite.spritecollideany(self.plane, self.aliens)
        if collision:
            self._plane_hit()
        
        self._check_aliens_leftedge()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width * 5, alien_height
        while current_y < (self.settings.screen_height - 2 * alien_height):
            while current_x < self.settings.screen_width - alien_width * 2:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finish a row; reset x value, and increment y value.
            current_x = alien_width * 5
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and put it in the row."""
        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Response appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Forward the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_forward_speed
        self.settings.fleet_direction *= -1

    def _plane_hit(self):
        """Respond to the ship being hit by an alien."""
        # Create an explosion at the center of the plane
        explosion = Explosion(self.plane.rect.center, self, scale=2)
        self.explosions.add(explosion)
        # Wait for the explosion animation to finish
        while self.explosions:
            self._update_screen()
            self.explosions.update()
            self.alien_hit_sound.play()
            self.clock.tick(60)  # Maintain the frame rate
        sleep(2.5)

        if self.stats.plane_left > 0:
            # Decrement plane_left, and update scoreboard.
            self.stats.plane_left -= 1
            self.sb.prep_planes()
            # Get rid of any remaining bullets and aliens.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the plane.
            self._create_fleet()
            self.plane.center_plane()
        else:
            self.game_active = False
            # pygame.mouse.set_visible(True)

    def _check_aliens_leftedge(self):
        for alien in self.aliens.sprites():
            if alien.rect.x <= 0:
                self._plane_hit()
                break
    
    def _create_buttons(self):
        """Create all buttons."""
        # Define button labels
        button_data = ["EASY", "NORMAL", "HARD", "HELL", "W/F", "QUIT"]
        # Create buttons dynamically
        spacing = 72
        self.buttons = []  # Store all buttons in a list
        for index, label in enumerate(button_data):  # Use enumerate to get the index
            button = Button(self, label)  # Use default color
            if label == "QUIT" or label == "W/F":
                button.rect.y = 240 + index * spacing
            else:
                button.rect.y = 200 + index * spacing
            button.msg_image_rect.center = button.rect.center
            self.buttons.append(button)

        # Assign buttons to specific attributes for easy access
        self.easy_button, self.normal_button, self.hard_button, self.hell_button, self.wf_button, self.quit_button  = self.buttons

    def _check_buttons(self, mouse_pos):
        """Start a new game when the player clicks one of the buttons."""
        if self.easy_button.rect.collidepoint(mouse_pos):
            self._start_game()
        elif self.normal_button.rect.collidepoint(mouse_pos):
            self._start_game()
            for each in range(8):
                self.settings.increase_speed()
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self._start_game()
            for each in range(18):
                self.settings.increase_speed()
        elif self.hell_button.rect.collidepoint(mouse_pos):
            self._start_game()
            for each in range(24):
                self.settings.increase_speed()
        elif self.wf_button.rect.collidepoint(mouse_pos):
            self._switch_window_fullscreen()
        elif self.quit_button.rect.collidepoint(mouse_pos):
            self._save_exit()

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings:
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.game_active = True
        self.sb._prep_images()

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.plane.center_plane()

        # Hide the mouse cursor.
        # pygame.mouse.set_visible(False)

    def _switch_window_fullscreen(self):
        """Switch between fullscreen and windowed mode."""
        self.settings.fullscreen = not self.settings.fullscreen
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))

    def _save_exit(self):
        """Save the high score to highscore.txt and exit."""
        path = Path("highscore.txt")
        if int(path.read_text()) < self.stats.high_score:
            path.write_text(str(self.stats.high_score))
        sys.exit()


if __name__ == '__main__':
    hg = Horizongame()
    hg.run_game()
