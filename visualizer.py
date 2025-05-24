import pygame
import cv2
import numpy as np
import os

class Button:
    """
    Represents a clickable button in the Pygame window.
    """
    def __init__(self, text, x, y, width, height, color=(200, 200, 200), text_color=(0, 0, 0)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36) # Default font for buttons

    def draw(self, surface):
        """
        Draws the button on the given Pygame surface.
        """
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10) # Rounded corners
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Checks if a given mouse position is within the button's bounds.
        """
        return self.rect.collidepoint(pos)

class Visualizer:
    """
    Handles all visual rendering for the game using Pygame and OpenCV.
    """
    def __init__(self, im1_path=None, im2_path=None):
        pygame.init() # Ensure Pygame is initialized

        # Get screen info after pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # Set window size based on screen resolution, leaving space for taskbar
        self.window_width = int(screen_width * 0.8) # Use 80% of screen width
        self.window_height = int(screen_height * 0.9) # Use 90% of screen height

        # Ensure minimum size to avoid display issues
        min_width = 800
        min_height = 600
        self.window_width = max(self.window_width, min_width)
        self.window_height = max(self.window_height, min_height)

        # Set the display mode to fixed size (remove RESIZABLE flag)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Squid Game: Lampu Merah Hijau")

        # Define heights for webcam and game area
        self.webcam_area_height = int(self.window_height * 0.5) # Approx 50% for webcam feed
        self.game_area_height = self.window_height - self.webcam_area_height # Remaining for game area

        # Fallback paths if not provided (though they should be from Game class)
        default_im1 = 'im1.png'
        default_im2 = 'im2.png'

        try:
            # Load and scale background images for the game area (bottom part)
            self.background_green_img_original = pygame.image.load(im1_path if im1_path else default_im1).convert()
            self.background_red_img_original = pygame.image.load(im2_path if im2_path else default_im2).convert()
            # Scale them initially to fit the new fixed window dimensions
            self.background_green_img = pygame.transform.scale(self.background_green_img_original, (self.window_width, self.game_area_height))
            self.background_red_img = pygame.transform.scale(self.background_red_img_original, (self.window_width, self.game_area_height))
        except pygame.error as e:
            print(f"Error loading background images: {e}. Using solid colors.")
            self.background_green_img_original = pygame.Surface((self.window_width, self.game_area_height))
            self.background_green_img_original.fill((0, 255, 0))
            self.background_red_img_original = pygame.Surface((self.window_width, self.game_area_height))
            self.background_red_img_original.fill((255, 0, 0))
            self.background_green_img = self.background_green_img_original
            self.background_red_img = self.background_red_img_original


        self.font_large = pygame.font.Font(None, 60) # Increased font size for main notifications
        self.font_medium = pygame.font.Font(None, 36) # For smaller text like timers
        self.font_small = pygame.font.Font(None, 28) # For smaller prompts like "Press S to start"


    def _convert_opencv_frame_to_pygame(self, cv_frame):
        """
        Converts an OpenCV BGR frame to a Pygame Surface, scaled to webcam area.
        """
        # Flip frame horizontally for selfie-view
        cv_frame = cv2.flip(cv_frame, 1)
        # Convert BGR to RGB
        cv_frame = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2RGB)
        # Resize to target size for the webcam display area
        cv_frame = cv2.resize(cv_frame, (self.window_width, self.webcam_area_height))
        # Convert to Pygame surface
        pygame_surface = pygame.surfarray.make_surface(cv_frame.swapaxes(0, 1))
        return pygame_surface


    def draw(self, cv_frame, player, environment, notification="", buttons=None, game_started=False):
        """
        Draws all game elements on the Pygame screen.
        cv_frame: The raw OpenCV frame from the webcam.
        player: Player object.
        environment: Environment object.
        notification: Text message to display.
        buttons: List of Button objects to draw.
        game_started: Boolean to indicate if the game has started (affects what's drawn).
        """
        self.screen.fill((0, 0, 0)) # Clear screen with black

        # Draw webcam feed (top area)
        webcam_surface = self._convert_opencv_frame_to_pygame(cv_frame)
        self.screen.blit(webcam_surface, (0, 0))

        # Draw remaining game time on the webcam feed area (top-left)
        remaining_time_text = f"Waktu Tersisa: {int(environment.get_remaining_game_time())} detik"
        time_surface = self.font_medium.render(remaining_time_text, True, (255, 255, 255)) # White text
        self.screen.blit(time_surface, (20, 20)) # Top-left corner

        # Draw notifications on the webcam feed area (centered horizontally, below time)
        notification_surface = self.font_large.render(notification, True, (255, 255, 255)) # White text
        # Adjusted Y position for notification to be lower than time
        notification_rect = notification_surface.get_rect(center=(self.window_width // 2, self.webcam_area_height // 2 + 50))
        self.screen.blit(notification_surface, notification_rect)

        # Draw buttons if provided (e.g., in initial state)
        if buttons:
            for button in buttons:
                button.draw(self.screen)
        
        # --- Draw game elements ONLY if game has started ---
        if game_started:
            # Draw game background (bottom area)
            game_background = self.background_green_img if environment.is_green_light() else self.background_red_img
            self.screen.blit(game_background, (0, self.webcam_area_height)) # Start game background after webcam area

            # --- Draw player character on top of the game background ---
            player_frame_rgba = player.get_current_frame()
            if player_frame_rgba is not None:
                # Convert RGBA NumPy array to Pygame Surface with alpha
                player_surface = pygame.image.frombuffer(player_frame_rgba.tobytes(), player_frame_rgba.shape[1::-1], "RGBA")
                
                # Calculate absolute position for Mario on the screen
                # player.x is relative to the game area (0 to window_width)
                # player.y is relative to the game area (0 to game_area_height)
                # So, the blit position is (player.x, self.webcam_area_height + player.y)
                self.screen.blit(player_surface, (int(player.x), int(self.webcam_area_height + player.y)))
            # --- End Draw player character ---

            '''
            # Draw finish line
            finish_line_color = (0, 0, 0) # Blue
            
            # Explicitly cast coordinates to int to prevent any potential TypeError
            line_start_x = int(environment.finish_line_x)
            line_start_y = int(self.webcam_area_height) # Top of the game area
            line_end_x = int(environment.finish_line_x)
            line_end_y = int(self.window_height) # Bottom of the window
            
           #  pygame.draw.line(self.screen, finish_line_color,
           #                  (line_start_x, line_start_y),
           #                  (line_end_x, line_end_y), 5)
           
            '''
            
            # Draw "Red Light" or "Green Light" text in the game area (bottom part)
            if environment.is_red_light():
                light_text_surface = self.font_large.render("Red Light", True, (255, 0, 0)) # Red text
            elif environment.is_green_light():
                light_text_surface = self.font_large.render("Green Light", True, (0, 255, 0)) # Green text
            else:
                light_text_surface = None

            if light_text_surface:
                # Center the light status text within the game area
                light_text_rect = light_text_surface.get_rect(center=(self.window_width // 2, self.webcam_area_height + self.game_area_height // 2))
                self.screen.blit(light_text_surface, light_text_rect)
        else:
            # If game not started, draw a black background for the game area
            # to hide Mario, finish line, and red/green light text
            black_background_for_game_area = pygame.Surface((self.window_width, self.game_area_height))
            black_background_for_game_area.fill((0,0,0))
            self.screen.blit(black_background_for_game_area, (0, self.webcam_area_height))


        pygame.display.flip() # Update the full display

    def display_final_message(self, result_text, save_button=None, restart_button=None, exit_button=None):
        """
        Displays the final game result and video save status using Pygame.
        Now includes buttons for saving video and restarting.
        """
        # Create a new surface for the message
        message_surface_width = int(self.window_width * 0.9)
        message_surface_height = int(self.window_height * 0.4)
        message_surface = pygame.Surface((message_surface_width, message_surface_height))
        message_surface.fill((255, 255, 255)) # White background

        # Render texts
        font_title = pygame.font.Font(None, 50)
        font_result = pygame.font.Font(None, 40)
        font_video = pygame.font.Font(None, 30)

        title_text = font_title.render("--- Hasil Permainan ---", True, (0, 0, 0))
        result_line = font_result.render(result_text, True, (0, 0, 255))

        # Position texts relative to message_surface
        message_surface.blit(title_text, title_text.get_rect(center=(message_surface.get_width() // 2, 50)))
        message_surface.blit(result_line, result_line.get_rect(center=(message_surface.get_width() // 2, 120)))

        # Blit the message surface onto the main screen, centered
        self.screen.fill((0, 0, 0)) # Clear main screen
        self.screen.blit(message_surface, message_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))) # Move message up slightly

        # Draw buttons on the main screen, below the message surface
        # Position buttons relative to the screen center for better layout
        button_y_pos = self.window_height // 2 + 100
        if save_button: # This will be None in current setup
            save_button.rect.center = (self.window_width // 2 - 180, button_y_pos)
            save_button.draw(self.screen)
        if restart_button:
            # If save_button is None, position restart_button more centrally
            if save_button is None:
                restart_button.rect.center = (self.window_width // 2 - 100, button_y_pos)
            else:
                restart_button.rect.center = (self.window_width // 2 - 100, button_y_pos) # Adjust if there's a save button
            restart_button.draw(self.screen)
        if exit_button:
            # If save_button is None, position exit_button more centrally
            if save_button is None:
                exit_button.rect.center = (self.window_width // 2 + 100, button_y_pos)
            else:
                exit_button.rect.center = (self.window_width // 2 + 100, button_y_pos) # Adjust if there's a save button
            exit_button.draw(self.screen)

        pygame.display.flip() # Update the full display

