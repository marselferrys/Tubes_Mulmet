import time
import numpy as np

class Environment:
    """
    Manages game rules, light status (green/red), timers,
    and win/lose conditions related to the game environment.
    """
    def __init__(self, window_width=800, green_duration_range=(2, 5), red_duration_range=(1, 3), game_duration_range=(50, 61)):
        self.finish_line_x = window_width - 160 # Adjust this value based on exact doll position
        self.light_status = "initial" # Can be "initial", "green", "red"
        self.green_duration_range = green_duration_range
        self.red_duration_range = red_duration_range # Fixed duration for red light
        self.game_duration_range = game_duration_range

        self.green_duration = 0
        self.green_start_time = 0
        self.red_duration = 0 # Fixed duration for red light, sebelumnya 3
        self.red_light_start_time = 0

        self.game_start_time = 0
        self.total_game_duration = 0
        
        self.paused_time_total = 0
        self.pause_start_time = None
        self.is_paused = False
        
        self.green_paused_time = 0
        self.green_pause_start = None

        self.red_paused_time = 0
        self.red_pause_start = None

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
        
        self.is_paused = False
        self.pause_start_time = None
        self.paused_time_total = 0

        self.green_paused_time = 0
        self.green_pause_start = None

        self.red_paused_time = 0
        self.red_pause_start = None

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
        self.green_paused_time = 0
        self.green_pause_start = None
        print(f"Green Light for {self.green_duration} seconds.")

    def switch_to_red_light(self):
        """
        Switches the light status to red and sets its duration.
        """
        self.light_status = "red"
        self.red_light_start_time = time.time()
        self.red_duration = np.random.randint(*self.red_duration_range)
        self.red_paused_time = 0
        self.red_pause_start = None
        print(f"Red Light for {self.red_duration_range} seconds.")

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
        if self.is_green_light():
            if self.is_paused:
                elapsed = self.green_pause_start - self.green_start_time - self.green_paused_time
            else:
                elapsed = time.time() - self.green_start_time - self.green_paused_time
            return max(0, self.green_duration - elapsed)
        return 0

    def get_remaining_red_time(self):
        if self.is_red_light():
            if self.is_paused:
                elapsed = self.red_pause_start - self.red_light_start_time - self.red_paused_time
            else:
                elapsed = time.time() - self.red_light_start_time - self.red_paused_time
            return max(0, self.red_duration - elapsed)
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
        return self.is_red_light() and (time.time() - self.red_light_start_time) >= self.red_duration

    def get_remaining_game_time(self):
        if self.game_start_time == 0:
            return self.total_game_duration
        if self.is_paused:
            elapsed = self.pause_start_time - self.game_start_time - self.paused_time_total
        else:
            elapsed = time.time() - self.game_start_time - self.paused_time_total
        return max(0, self.total_game_duration - elapsed)

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
        return player_x > self.finish_line_x + 20

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.pause_start_time = time.time()

            if self.is_green_light():
                self.green_pause_start = time.time()
            elif self.is_red_light():
                self.red_pause_start = time.time()

    def resume(self):
        if self.is_paused:
            pause_duration = time.time() - self.pause_start_time
            self.paused_time_total += pause_duration

            if self.is_green_light() and self.green_pause_start is not None:
                self.green_paused_time += time.time() - self.green_pause_start

            if self.is_red_light() and self.red_pause_start is not None:
                self.red_paused_time += time.time() - self.red_pause_start

            self.is_paused = False
            self.pause_start_time = None
            self.green_pause_start = None
            self.red_pause_start = None