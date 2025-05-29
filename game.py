#import semua modul eksternal dan internal yang di butuhkan
import pygame
import cv2
import time
import numpy as np
import os

# Import semua komponen game yang diperlukan
from player import Player
from environment import Environment
from input_handler import InputHandler
from visualizer import Visualizer, Button
from sound_manager import SoundManager
from utils import is_visible

#ambil path direktori utama tempat script dijalankan (main.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#tentukan direktori aset game
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class Game:
    """
    Kelas utama yang mengatur seluruh alur permainan, termasuk logika game loop, input pengguna, deteksi webcam, suara, dan visualisasi.
    """
    def __init__(self):
        # insialisasi Pygame dan font
        pygame.init()
        pygame.font.init()
        # inisialisasi semua komponen game

        self.sound_manager = SoundManager(assets_dir=ASSETS_DIR)
        self.input_handler = InputHandler()
        self.player = Player(gif_path=os.path.join(ASSETS_DIR, 'mario.gif'))
        self.environment = Environment()
        self.visualizer = Visualizer(im1_path=os.path.join(ASSETS_DIR, 'im1.png'),
                                     im2_path=os.path.join(ASSETS_DIR, 'im2.png'))
        
        self.environment = Environment(window_width=self.visualizer.window_width)

        # tentukan posisi awal karakter pemain
        player_game_area_y = self.visualizer.game_area_height - self.player.character_height
        self.player.y = player_game_area_y
        self.player.initial_y = player_game_area_y # digunakan untuk reset posisi

        # inisialisasi webcam untuk menangkap input pengguna
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("ERROR: Tidak dapat mengakses webcam. Pastikan webcam terhubung dan tidak digunakan oleh aplikasi lain.")
            self.is_running = False
            return

        #parameter kontrol game
        self.is_running = True
        self.game_started = False
        self.game_over = False
        self.winner = False
        self.paused = False
        self.user_body_sum_red_light = 0

        self.movement_speed = 15
        self.threshold_dist_body = 180
        self.min_sound_threshold_to_move = 0.01
        self.max_sound_volume = 0.2

        # Inisialisasi notifikasi awal dan tombol
        self.notification = "Tekan 'S' untuk memulai\nTekan Spasi untuk Pause"
        self.buttons = [
            Button("Start (S)", self.visualizer.window_width // 2 - 150, self.visualizer.window_height - 100, 150, 50),
            Button("Quit (Q)", self.visualizer.window_width // 2 + 50, self.visualizer.window_height - 100, 150, 50)
        ]
        self.red_light_delay_start_time = 0
        self.play_again_button = Button("Play Again", self.visualizer.window_width // 2 - 100, self.visualizer.window_height // 2 + 100, 150, 50)
        self.exit_button = Button("Exit", self.visualizer.window_width // 2 + 100, self.visualizer.window_height // 2 + 100, 150, 50)


    def handle_input(self):
        """
        tangani event dari keybord atau mouse, ambil frame dari webcam, dan proses input pengguna
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                # Tombol spasi untuk pause/resume (hanya jika game berjalan dan belum game over)
                if event.key == pygame.K_SPACE and self.game_started and not self.game_over:
                    self.paused = not self.paused
                    if self.paused:
                        self.environment.pause()
                        self.notification = "Permainan Dijeda. Tekan Spasi untuk Melanjutkan."
                    else:
                        self.environment.resume()
                        self.notification = "Permainan Dilanjutkan!"

                # Tombol 'S' dan 'Q' hanya jika belum dimulai dan belum game over
                elif not self.game_started and not self.game_over:
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


        # Ambil frame dari webcam dan proses landmark tubuh
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
        Memulai game baru, reset posisi pemain dan status game
        """
        self.game_started = True
        self.game_over = False
        self.winner = False
        self.player.reset_position()
        self.environment.reset() 
        self.environment.start_game_timer()
        self.environment.switch_to_green_light()
        self.sound_manager.play_sound('green_light')
        
        self.notification = "Green Light!"
        self.user_body_sum_red_light = 0

    def reset_game(self):
        """
        Mengembalikan game ke posisi awal
        """
        self.game_started = False
        self.game_over = False
        self.winner = False
        self.player.reset_position()
        self.environment.reset()
        self.notification = "Tekan 'S' atau tombol 'Start' untuk memulai"
        self.user_body_sum_red_light = 0

    def check_win_lose_conditions(self, current_game_time):
        """
        Mengecek kondisi menang atau kalah berdasarkan posisi pemain dan waktu permainan.
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
        Main loop dari permainan 
        """
        self.is_running = True # Ensure this session starts as running
        while self.is_running:
            frame, results = self.handle_input()
            if not self.is_running or frame is None:
                break

            # Gambar pose Landmark
            frame_with_landmarks = self.input_handler.draw_landmarks(frame.copy(), results)

            #Menampilkan halaman awal jika game belum dimulai
            if not self.game_started:
                self.visualizer.draw(frame_with_landmarks, self.player, self.environment,
                                     notification=self.notification, buttons=self.buttons, game_started=False)
                self.player.update_animation_frame()
                continue
            
            # Jika game dijeda
            if self.paused:
                self.visualizer.draw(frame_with_landmarks, self.player, self.environment,
                                    notification=self.notification, game_started=True)
                self.player.update_animation_frame()
                continue

            # jika game sudah selesai
            if self.game_over:
                self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                self.is_running = False
                continue

            # Cek apakah tubuh bagian atas terlihat di kamera  
            if results and results.pose_landmarks:
                if not is_visible(results.pose_landmarks.landmark):
                    self.notification = "Silakan pastikan tubuh bagian atas terlihat di kamera"
                    self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                    continue
                else:
                    self.notification = ""

            # Logika saat lampu hijau
            if self.environment.is_green_light():
                if not self.paused and self.environment.is_green_light_over():
                    self.notification = "Bersiap untuk Red Light..."
                    self.red_light_delay_start_time = time.time()
                    self.environment.light_status = "transition_to_red"
                    self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)
                    self.sound_manager.play_sound('red_light')
                    continue

                # Ambil volume dan pitch dari suara pengguna
                sound_volume, sound_pitch  = self.input_handler.get_user_voice_volume_and_pitch()
                # Deteksi apakah suara cukup kuat untuk bergerak
                sound_detected = sound_volume > self.min_sound_threshold_to_move
                # Default multiplier 
                sound_speed_multiplier = 0.0
                
                if sound_detected:
                   # Normalisasi volume ke rentang [0.0, 1.5]
                    normalized_volume = min(1.5, (sound_volume - self.min_sound_threshold_to_move) / (self.max_sound_volume - self.min_sound_threshold_to_move))

                    # Gunakan pitch untuk mempengaruhi multiplier, misalnya pitch 100–800 Hz → 0–5
                    pitch_multiplier = min(5.0, max(0.0, (sound_pitch - 100) / 140))  # normalisasi pitch ke 0-5

                    # Total multiplier gabungan dari volume dan pitch
                    sound_speed_multiplier = normalized_volume * pitch_multiplier
                    
                # Set kecepatan gerak dasar
                current_movement_speed = self.movement_speed
                
                # Jika suara terdeteksi, gerakan karakter
                if not self.paused and sound_detected:
                    current_movement_speed += sound_speed_multiplier
                    self.notification = f"Gerak! Suara terdeteksi: {sound_volume:.2f}, Pitch: {sound_pitch:.2f} Hz"
                    self.player.move(current_movement_speed, self.environment.finish_line_x)
                    self.player.update_animation_frame()
                else:
                    self.notification = "Bersuara untuk Maju!"
                    self.player.update_animation_frame()
                    
            elif self.environment.light_status == "transition_to_red":
                # Transisi dari hijau ke merah
                if (time.time() - self.red_light_delay_start_time) >= 0.5:
                    self.environment.switch_to_red_light()
                    self.notification = "Red Light! Jangan Bersuara!"
                else:
                    self.notification = "Bersiap untuk Red Light..."

            elif self.environment.is_red_light():
                if not self.paused and self.environment.is_red_light_over():
                    self.environment.switch_to_green_light()
                    self.sound_manager.play_sound('green_light')
                    self.notification = "Green Light!"
                else:
                    sound_volume, sound_pitch = self.input_handler.get_user_voice_volume_and_pitch()
                    sound_detected_red_light = sound_volume > self.min_sound_threshold_to_move

                    if not self.paused and sound_detected_red_light:
                        self.game_over = True
                        self.notification = f"Kamu Kalah: Bersuara (Volume: {sound_volume:.2f}, Pitch: {sound_pitch:.2f} Hz)"
                        self.sound_manager.play_sound('lose')
                        print(self.notification)
                    else:
                        self.notification = "Red Light! Jangan Bersuara!"

            self.player.update_animation_frame()
            self.check_win_lose_conditions(time.time())

            self.visualizer.draw(frame_with_landmarks, self.player, self.environment, notification=self.notification, game_started=True)

        self.cap.release()
        
        play_again = False

        final_result_text = "Permainan berakhir."
        if self.winner:
            final_result_text = "Selamat! Kamu Menang."
        elif self.game_over:
            final_result_text = self.notification

        # Tampilkan layar akhir permainan dengan pesan hasil dan dua tombol: restart dan keluar
        self.visualizer.display_final_message(final_result_text,
                                                  save_button=None, 
                                                  restart_button=self.play_again_button,
                                                  exit_button=self.exit_button)

        # Tunggu input pengguna di layar akhir
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
                    if event.key == pygame.K_r: # Tekan R untuk main lagi
                        print("Memulai ulang permainan...")
                        play_again = True
                        waiting_for_choice = False
                    elif event.key == pygame.K_q: # Tekan Q untuk keluar
                        print("Keluar dari permainan.")
                        play_again = False
                        waiting_for_choice = False

        # Keluar dari pygame setelah pengguna memilih
        pygame.quit()
        return play_again
