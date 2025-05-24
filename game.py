import pygame
import cv2
import time
import numpy as np
import os

from player import Player
from environment import Environment
from input_handler import InputHandler
from visualizer import Visualizer, Button
from sound_manager import SoundManager
from utils import calculate_sum, is_visible

# Get the absolute path of the directory where this script (main.py) is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the assets directory relative to the base directory
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class Game:
    """
    Main game class that orchestrates all components and manages the game loop.
    """
    def __init__(self):
        pygame.init()
        pygame.font.init() # Initialize the font module explicitly here

        self.sound_manager = SoundManager(assets_dir=ASSETS_DIR)
        self.input_handler = InputHandler()
        self.player = Player(gif_path=os.path.join(ASSETS_DIR, 'mario.gif'))
        self.environment = Environment()
        self.visualizer = Visualizer(im1_path=os.path.join(ASSETS_DIR, 'im1.png'),
                                     im2_path=os.path.join(ASSETS_DIR, 'im2.png'))
        
        self.environment = Environment(window_width=self.visualizer.window_width)

        # Calculate player's starting Y position after visualizer is initialized
        player_game_area_y = self.visualizer.game_area_height - self.player.character_height
        self.player.y = player_game_area_y
        self.player.initial_y = player_game_area_y # Update initial_y for reset


        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("ERROR: Tidak dapat mengakses webcam. Pastikan webcam terhubung dan tidak digunakan oleh aplikasi lain.")
            self.is_running = False
            return

        self.is_running = True
        self.game_started = False
        self.game_over = False
        self.winner = False
        self.paused = False

        self.prev_hand_pos = None
        self.user_body_sum_red_light = 0

        self.movement_speed = 15
        self.threshold_dist_body = 180
        self.min_sound_threshold_to_move = 0.01
        self.max_sound_volume = 0.2

        self.notification = "Tekan 'S' atau tombol 'Start' untuk memulai"
        self.buttons = [
            Button("Start (S)", self.visualizer.window_width // 2 - 150, self.visualizer.window_height - 100, 150, 50),
            Button("Quit (Q)", self.visualizer.window_width // 2 + 50, self.visualizer.window_height - 100, 150, 50)
        ]
        self.red_light_delay_start_time = 0

        self.play_again_button = Button("Play Again", self.visualizer.window_width // 2 - 100, self.visualizer.window_height // 2 + 100, 150, 50)
        self.exit_button = Button("Exit", self.visualizer.window_width // 2 + 100, self.visualizer.window_height // 2 + 100, 150, 50)


    def handle_input(self):
        """
        Processes Pygame events (keyboard, mouse) and captures a webcam frame.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if not self.game_started and not self.game_over:
                    if event.key == pygame.K_s:
                        self.start_game()
                    elif event.key == pygame.K_q:
                        self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(pos):
                            if button.text.startswith("Start"):
                                self.start_game()
                            elif button.text.startswith("Quit"):
                                self.is_running = False

        ret, frame = self.cap.read()
        if not ret:
            print("Gagal mengambil frame dari webcam.")
            self.is_running = False
            return None, None

        frame = cv2.blur(frame, (5, 5))
        results = self.input_handler.process_frame(frame)
        return frame, results

    def start_game(self):
        """
        Initializes game state for a new round.
        """
        self.game_started = True
        self.game_over = False
        self.winner = False
        self.player.reset_position()
        self.environment.reset() # Reset environment timers and light status
        self.environment.start_game_timer()
        self.environment.switch_to_green_light()
        self.sound_manager.play_sound('green_light')
        
        self.notification = "Green Light!"
        self.prev_hand_pos = None
        self.user_body_sum_red_light = 0

    def reset_game(self):
        """
        Resets the game to its initial state (start screen).
        """
        self.game_started = False
        self.game_over = False
        self.winner = False
        self.player.reset_position()
        self.environment.reset()
        self.notification = "Tekan 'S' atau tombol 'Start' untuk memulai"
        self.prev_hand_pos = None
        self.user_body_sum_red_light = 0

    def check_win_lose_conditions(self, current_game_time):
        """
        Checks if the player has won, lost due to time, or lost due to red light violation.
        """
        if self.environment.reached_finish_line(self.player.x):
            self.winner = True
            self.game_over = True
            self.notification = "Selamat! Kamu Menang."
            self.sound_manager.play_sound('win')
            return True
        if self.environment.has_game_time_elapsed():
            self.game_over = True
            self.notification = "Waktu Habis! Kamu Kalah."
            self.sound_manager.play_sound('lose')
            return True
        return False

    def run(self):
        """
        The main game loop for a single session.
        Returns True if the user wants to play again, False otherwise.
        """
        self.is_running = True # Ensure this session starts as running
        while self.is_running:
            frame, results = self.handle_input()
            if not self.is_running or frame is None:
                break

            # Draw landmarks on the frame (for webcam display)
            frame_with_landmarks = self.input_handler.draw_landmarks(frame.copy(), results)

            # Initial state: waiting for game to start
            if not self.game_started:
                self.visualizer.draw(frame_with_landmarks, self.player, self.environment,
                                     notification=self.notification, buttons=self.buttons, game_started=False)
                self.player.update_animation_frame()
                continue

            # Game Over state: If game is over, break the main loop
            if self.game_over:
                self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                self.is_running = False
                continue


            # Check if user is in frame (still relevant for webcam display and general game flow)
            if results and results.pose_landmarks:
                if not is_visible(results.pose_landmarks.landmark):
                    self.notification = "Silakan pastikan tubuh bagian atas terlihat di kamera"
                    self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                    continue
                else:
                    self.notification = ""

            # Game logic based on light status
            if self.environment.is_green_light():
                if self.environment.is_green_light_over():
                    self.notification = "Bersiap untuk Red Light..."
                    self.red_light_delay_start_time = time.time()
                    self.environment.light_status = "transition_to_red"
                    self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                    self.sound_manager.play_sound('red_light')
                    continue

                sound_volume = self.input_handler.get_user_voice_volume()
                sound_detected = sound_volume > self.min_sound_threshold_to_move
                sound_speed_multiplier = 0.0
                if sound_volume > self.min_sound_threshold_to_move:
                    normalized_volume = min(1.0, (sound_volume - self.min_sound_threshold_to_move) / (self.max_sound_volume - self.min_sound_threshold_to_move))
                    sound_speed_multiplier = normalized_volume * 3.0

                current_movement_speed = self.movement_speed
                
                if sound_detected:
                    current_movement_speed += sound_speed_multiplier
                    self.notification = f"Bergerak Maju! Suara: {sound_volume:.2f}"
                    self.player.move(current_movement_speed, self.environment.finish_line_x)
                    self.player.update_animation_frame()
                else:
                    self.notification = "Bersuara untuk Maju!"
                    self.player.update_animation_frame()


            elif self.environment.light_status == "transition_to_red":
                if (time.time() - self.red_light_delay_start_time) >= 0.5:
                    self.environment.switch_to_red_light()
                    self.notification = "Red Light! Jangan Bersuara!"
                else:
                    self.notification = "Bersiap untuk Red Light..."

            elif self.environment.is_red_light():
                if self.environment.is_red_light_over():
                    self.environment.switch_to_green_light()
                    self.sound_manager.play_sound('green_light')
                    self.notification = "Green Light!"
                else:
                    sound_volume = self.input_handler.get_user_voice_volume()
                    sound_detected_red_light = sound_volume > self.min_sound_threshold_to_move

                    if sound_detected_red_light:
                        self.game_over = True
                        self.notification = "Kamu Kalah: Bersuara saat lampu merah!"
                        self.sound_manager.play_sound('lose')
                        print(self.notification)
                    else:
                        self.notification = "Red Light! Jangan Bersuara!"

            self.player.update_animation_frame()
            self.check_win_lose_conditions(time.time())

            self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)

        self.cap.release()
        
        # video_saved_message = "Video tidak disimpan." # Always "Video tidak disimpan."
        play_again = False

        final_result_text = "Permainan berakhir."
        if self.winner:
            final_result_text = "Selamat! Kamu Menang."
        elif self.game_over:
            final_result_text = self.notification

        # Draw the final message screen with only restart/exit buttons
        self.visualizer.display_final_message(final_result_text,
                                                  save_button=None, # No save button
                                                  restart_button=self.play_again_button,
                                                  exit_button=self.exit_button)

        # Wait for user input on the final screen
        waiting_for_choice = True
        while waiting_for_choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_choice = False
                    play_again = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.play_again_button.is_clicked(pos):
                        print("Memulai ulang permainan...")
                        play_again = True
                        waiting_for_choice = False
                    elif self.exit_button.is_clicked(pos):
                        print("Keluar dari permainan.")
                        play_again = False
                        waiting_for_choice = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Restart with R key
                        print("Memulai ulang permainan...")
                        play_again = True
                        waiting_for_choice = False
                    elif event.key == pygame.K_q: # Quit with Q key
                        print("Keluar dari permainan.")
                        play_again = False
                        waiting_for_choice = False

        pygame.quit()
        return play_again
