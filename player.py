import numpy as np
from utils import load_gif_frames # memuat fungsi load_gif_frames dari utils.py


class Player:
    """
    Representasi karakter pemain dalam permainan (misalnya mario).
    """
    def __init__(self, start_x=55, start_y=None, gif_path=None, game_area_height=550): # start_y will be calculated and set by Game
        """
        Inisialisasi objek Player.

        Args:
            start_x (int): Posisi horizontal awal.
            start_y (int): Posisi vertikal awal (jika None, dihitung otomatis berdasarkan tinggi game area).
            gif_path (str): Path ke file GIF animasi karakter.
            game_area_height (int): Tinggi area permainan (untuk posisi vertikal jika start_y=None).
        """
        self.x = start_x
        self.y = start_y
        self.initial_x = start_x # posisi awal x untuk reset
        self.initial_y = start_y # posisi awal y untuk reset

        self.gif_path = gif_path if gif_path else 'mario.gif' # Gunakan default path jika tidak diberikan
        self.frames = load_gif_frames(self.gif_path) # Muat seluruh frame dari GIF animasi
        self.frame_index = 0 # Indeks frame saat ini dalam animasi
        self.total_frames = len(self.frames) # Total jumlah frame dalam animasi
        self.character_width = 0
        self.character_height = 0
        if self.frames:
            self.character_height, self.character_width, _ = self.frames[0].shape
            if start_y is None: # jika start_y tidak diberikan, atur posisi y agar karakter berada di bawah area permainan
                self.y = game_area_height  - self.character_height 
                self.initial_y = self.y

    def get_current_frame(self):
        # Mengembalikan frame animasi saat ini dalam format array Numpy RGBA
        if self.frames:
            return self.frames[self.frame_index % self.total_frames]
        return None

    def update_animation_frame(self):
        # Memperbarui indeks frame untuk animasi karakter. (bergerak ke frame berikutnya)
        self.frame_index += 1

    def move(self, speed, max_x):
        # Menggerakkan pemain secara horizontal sebesar 'speed'. Memastikan pemain tidak keluar dari batas kanan area permainan.
        self.x += speed 

    def get_position(self):
        # mengembalikan posisi (x, y) pemain relatif terhadap kiri atas area permainan.
        return self.x, self.y

    def reset_position(self):
        # Mengembalikan posisi pemain ke posisi awal (initial_x, initial_y).
        self.x = self.initial_x
        self.y = self.initial_y 
        self.frame_index = 0 

