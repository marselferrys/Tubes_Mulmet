import time
import numpy as np

class Environment:
    """
    Manages game rules, light status (green/red), timers,
    and win/lose conditions related to the game environment.
    """
    def __init__(self, window_width=800, green_duration_range=(2, 5), game_duration_range=(50, 61)):
        self.finish_line_x = window_width - 50 # Adjust this value based on exact doll position
        self.light_status = "initial" # Can be "initial", "green", "red"
        self.green_duration_range = green_duration_range
        self.game_duration_range = game_duration_range

        self.green_duration = 0
        self.green_start_time = 0
        self.red_light_duration = 3 # Fixed duration for red light
        self.red_light_start_time = 0

        self.game_start_time = 0
        self.total_game_duration = 0

    def reset(self):
        """
        Resets all environment parameters for a new game.
        """
        self.light_status = "initial"
        self.green_duration = 0
        self.green_start_time = 0
        self.red_light_start_time = 0
        self.game_start_time = 0
        self.total_game_duration = np.random.randint(*self.game_duration_range)

    def start_game_timer(self):
        """
        Starts the overall game timer.
        """
        self.game_start_time = time.time()

    def switch_to_green_light(self):
        """
        Switches the light status to green and sets its duration.
        """
        self.light_status = "green"
        self.green_start_time = time.time()
        self.green_duration = np.random.randint(*self.green_duration_range)
        print(f"Green Light for {self.green_duration} seconds.")

    def switch_to_red_light(self):
        """
        Switches the light status to red and sets its duration.
        """
        self.light_status = "red"
        self.red_light_start_time = time.time()
        print(f"Red Light for {self.red_light_duration} seconds.")

    def is_green_light(self):
        """
        Checks if the current light status is green.
        """
        return self.light_status == "green"

    def is_red_light(self):
        """
        Checks if the current light status is red.
        """
        return self.light_status == "red"

    def is_initial_state(self):
        """
        Checks if the game is in its initial waiting state.
        """
        return self.light_status == "initial"

    def get_remaining_green_time(self):
        """
        Returns the remaining time for the green light phase.
        """
        if self.is_green_light():
            return max(0, self.green_duration - (time.time() - self.green_start_time))
        return 0

    def get_remaining_red_time(self):
        """
        Returns the remaining time for the red light phase.
        """
        if self.is_red_light():
            return max(0, self.red_light_duration - (time.time() - self.red_light_start_time))
        return 0

    def is_green_light_over(self):
        """
        Checks if the green light phase has ended.
        """
        return self.is_green_light() and (time.time() - self.green_start_time) >= self.green_duration

    def is_red_light_over(self):
        """
        Checks if the red light phase has ended.
        """
        return self.is_red_light() and (time.time() - self.red_light_start_time) >= self.red_light_duration

    def get_remaining_game_time(self):
        """
        Returns the overall remaining game time.
        """
        if self.game_start_time == 0: # Game not started yet
            return self.total_game_duration
        return max(0, self.total_game_duration - (time.time() - self.game_start_time))

    def has_game_time_elapsed(self):
        """
        Checks if the total game time has elapsed.
        """
        if self.game_start_time == 0:
            return False # Game hasn't started
        return (time.time() - self.game_start_time) >= self.total_game_duration

    def reached_finish_line(self, player_x):
        """
        Checks if the player has reached the finish line.
        """
        return player_x >= self.finish_line_x
