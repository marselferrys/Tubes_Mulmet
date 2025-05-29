import pygame
import cv2
import numpy as np
import os

class Button:
    """
    Kelas untuk merepresentasikan tombol interaktif dalam tampilan Pygame.
    Digunakan untuk tombol seperti Start, Restart, Exit, dll.
    """
    def __init__(self, text, x, y, width, height, color=(200, 200, 200), text_color=(0, 0, 0)):
        """
        Inisialisasi tombol dengan teks, posisi, ukuran, dan warna.
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)  # Gunakan font default

    def draw(self, surface):
        """
        Menggambar tombol ke permukaan Pygame.
        """
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)  # Tombol dengan sudut membulat
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Mengecek apakah posisi klik mouse berada dalam area tombol.
        """
        return self.rect.collidepoint(pos)

class Visualizer:
    """
    Kelas untuk menangani semua tampilan visual permainan.
    Menggabungkan tampilan dari webcam (OpenCV) dan elemen permainan (Pygame).
    """
    def __init__(self, im1_path=None, im2_path=None):
        """
        Inisialisasi tampilan game, memuat gambar latar, dan mengatur area webcam serta permainan.
        """
        pygame.init()  # Wajib sebelum menggunakan fitur tampilan Pygame

        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # Ukuran jendela game berdasarkan resolusi layar pengguna
        self.window_width = max(int(screen_width * 0.8), 800)
        self.window_height = max(int(screen_height * 0.9), 600)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Squid Game: Lampu Merah Hijau")

        # Area tampilan webcam dan permainan
        self.webcam_area_height = int(self.window_height * 0.5)
        self.game_area_height = self.window_height - self.webcam_area_height

        # Gambar latar default jika tidak disediakan
        default_im1 = 'im1.png'
        default_im2 = 'im2.png'

        try:
            self.background_green_img_original = pygame.image.load(im1_path if im1_path else default_im1).convert()
            self.background_red_img_original = pygame.image.load(im2_path if im2_path else default_im2).convert()
            self.background_green_img = pygame.transform.scale(self.background_green_img_original, (self.window_width, self.game_area_height))
            self.background_red_img = pygame.transform.scale(self.background_red_img_original, (self.window_width, self.game_area_height))
        except pygame.error as e:
            print(f"Error loading background images: {e}. Using solid colors.")
            self.background_green_img = pygame.Surface((self.window_width, self.game_area_height))
            self.background_green_img.fill((0, 255, 0))
            self.background_red_img = pygame.Surface((self.window_width, self.game_area_height))
            self.background_red_img.fill((255, 0, 0))

        # Font untuk berbagai elemen UI
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

    def _convert_opencv_frame_to_pygame(self, cv_frame):
        """
        Mengonversi frame OpenCV (BGR) menjadi permukaan Pygame yang bisa ditampilkan.
        """
        cv_frame = cv2.flip(cv_frame, 1)  # Kamera depan (mirror view)
        cv_frame = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2RGB)
        cv_frame = cv2.resize(cv_frame, (self.window_width, self.webcam_area_height))
        return pygame.surfarray.make_surface(cv_frame.swapaxes(0, 1))

    def draw(self, cv_frame, player, environment, notification="", buttons=None, game_started=False):
        """
        Menangani semua tampilan yang muncul di layar:
        - Webcam (atas)
        - Notifikasi permainan
        - Area permainan dan karakter (bawah)
        """
        self.screen.fill((0, 0, 0))  # Kosongkan layar

        # --- TAMPILAN WEBCAM ---
        webcam_surface = self._convert_opencv_frame_to_pygame(cv_frame)
        self.screen.blit(webcam_surface, (0, 0))

        # Tampilkan sisa waktu
        remaining_time_text = f"Waktu Tersisa: {int(environment.get_remaining_game_time())} detik"
        time_surface = self.font_medium.render(remaining_time_text, True, (255, 255, 255))
        self.screen.blit(time_surface, (20, 20))

        # Tampilkan notifikasi permainan (centered)
        if notification:
            lines = notification.split("\n")
            y = self.webcam_area_height // 2 + 30
            for line in lines:
                text_surface = self.font_large.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.window_width // 2, y))
                self.screen.blit(text_surface, text_rect)
                y += 50

        # Tampilkan tombol (jika ada)
        if buttons:
            for button in buttons:
                button.draw(self.screen)

        # --- TAMPILAN AREA PERMAINAN (Jika permainan sudah dimulai) ---
        if game_started:
            game_background = self.background_green_img if environment.is_green_light() else self.background_red_img
            self.screen.blit(game_background, (0, self.webcam_area_height))

            # Tampilkan karakter pemain (Mario)
            player_frame_rgba = player.get_current_frame()
            if player_frame_rgba is not None:
                player_surface = pygame.image.frombuffer(player_frame_rgba.tobytes(), player_frame_rgba.shape[1::-1], "RGBA")
                self.screen.blit(player_surface, (int(player.x - 50), int(self.webcam_area_height + (player.y - 75))))

            # Tampilkan status lampu (merah/hijau)
            if environment.is_red_light():
                light_text_surface = self.font_large.render("Red Light", True, (255, 0, 0))
            elif environment.is_green_light():
                light_text_surface = self.font_large.render("Green Light", True, (0, 255, 0))
            else:
                light_text_surface = None

            if light_text_surface:
                light_text_rect = light_text_surface.get_rect(center=(self.window_width // 2, self.webcam_area_height + self.game_area_height // 2))
                self.screen.blit(light_text_surface, light_text_rect)
        else:
            # Jika game belum dimulai, kosongkan area game
            black_bg = pygame.Surface((self.window_width, self.game_area_height))
            black_bg.fill((0, 0, 0))
            self.screen.blit(black_bg, (0, self.webcam_area_height))

        pygame.display.flip()  # Perbarui seluruh tampilan

    def display_final_message(self, result_text, save_button=None, restart_button=None, exit_button=None):
        """
        Menampilkan pesan akhir setelah permainan selesai.
        Disertai dengan tombol simpan, ulangi, atau keluar.
        """
        message_surface_width = int(self.window_width * 0.9)
        message_surface_height = int(self.window_height * 0.4)
        message_surface = pygame.Surface((message_surface_width, message_surface_height))
        message_surface.fill((255, 255, 255))  # Background putih

        # Tampilkan teks hasil
        font_title = pygame.font.Font(None, 50)
        font_result = pygame.font.Font(None, 40)

        title_text = font_title.render("--- Hasil Permainan ---", True, (0, 0, 0))
        result_line = font_result.render(result_text, True, (0, 0, 255))

        message_surface.blit(title_text, title_text.get_rect(center=(message_surface.get_width() // 2, 50)))
        message_surface.blit(result_line, result_line.get_rect(center=(message_surface.get_width() // 2, 120)))

        # Tampilkan pesan di tengah layar
        self.screen.fill((0, 0, 0))
        self.screen.blit(message_surface, message_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50)))

        # Atur dan gambar tombol
        button_y_pos = self.window_height // 2 + 100
        if save_button:
            save_button.rect.center = (self.window_width // 2 - 180, button_y_pos)
            save_button.draw(self.screen)
        if restart_button:
            restart_button.rect.center = (self.window_width // 2 - 100, button_y_pos)
            restart_button.draw(self.screen)
        if exit_button:
            exit_button.rect.center = (self.window_width // 2 + 100, button_y_pos)
            exit_button.draw(self.screen)

        pygame.display.flip()  # Perbarui tampilan
