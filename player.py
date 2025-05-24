import numpy as np
from utils import load_gif_frames # paste_character is no longer used by Player for drawing


class Player:
    """
    Represents the player character (Mario) in the game.
    Handles its position, animation, and provides its current frame.
    """
    def __init__(self, start_x=55, start_y=None, gif_path=None, game_area_height=550): # start_y will be calculated and set by Game
        self.x = start_x
        self.y = start_y
        self.initial_x = start_x # Store initial position for reset
        self.initial_y = start_y # Store initial y for reset

        self.gif_path = gif_path if gif_path else 'mario.gif' # Fallback if not provided
        self.frames = load_gif_frames(self.gif_path) # Load using the provided path
        self.frame_index = 0
        self.total_frames = len(self.frames)
        self.character_width = 0
        self.character_height = 0
        if self.frames:
            self.character_height, self.character_width, _ = self.frames[0].shape
            if start_y is None: # Fallback if start_y is not provided (e.g. for testing Player alone)
                self.y = game_area_height  - self.character_height # Assuming 480px game area height
                self.initial_y = self.y

    def get_current_frame(self):
        """
        Returns the current animation frame of the player as an RGBA NumPy array.
        """
        if self.frames:
            return self.frames[self.frame_index % self.total_frames]
        return None

    def update_animation_frame(self):
        """
        Advances the animation frame.
        """
        self.frame_index += 1

    def move(self, speed, max_x):
        """
        Moves the player horizontally by a given speed,
        ensuring it doesn't go beyond max_x.
        """
        self.x += speed 
        # Ensure player does not go beyond the right edge of the game area
        # if self.x + self.character_width >= max_x + 1:
        #    self.x = max_x - self.character_width

    def get_position(self):
        """
        Returns the current (x, y) position of the player (relative to game area top-left).
        """
        return self.x, self.y

    def reset_position(self):
        """
        Resets the player's position to its initial starting point.
        """
        self.x = self.initial_x
        self.y = self.initial_y # Reset y position as well
        self.frame_index = 0 # Reset animation as well

