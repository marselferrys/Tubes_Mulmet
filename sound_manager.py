import pygame
import time
import os

class SoundManager:
    """
    Mengelola pemutaran suara menggunakan Pygame mixer.
    """

    def __init__(self, assets_dir="."):  # Menerima path direktori aset suara
        pygame.mixer.init()  # Inisialisasi sistem audio Pygame

        # Menyimpan path lengkap ke file audio dalam sebuah dictionary
        self.sounds = {
            'green_light': os.path.join(assets_dir, 'greenLight.mp3'),  # Suara saat lampu hijau
            'red_light': os.path.join(assets_dir, 'redLight.mp3'),      # Suara saat lampu merah
            'win': os.path.join(assets_dir, 'win.mp3'),                 # Suara saat menang
            'lose': os.path.join(assets_dir, 'lose.mp3')                # Suara saat kalah
        }

    def play_sound(self, sound_name):
        """
        Memutar suara tertentu berdasarkan nama yang diberikan.
        """
        file_path = self.sounds.get(sound_name)  # Ambil path file berdasarkan nama
        if file_path:
            if not os.path.exists(file_path):
                # Jika file tidak ditemukan, tampilkan peringatan
                print(f"Peringatan: File suara tidak ditemukan di '{file_path}'.")
                return

            try:
                # Buat objek suara dari file
                sound = pygame.mixer.Sound(file_path)
                sound.play()  # Putar suara

                # Tunggu hingga suara selesai dimainkan (opsional, bisa dihapus untuk musik latar)
                while pygame.mixer.get_busy():
                    time.sleep(0.01)  # Delay kecil agar tidak membebani CPU
            except pygame.error as e:
                # Tangani error jika file tidak bisa diputar
                print(f"Error saat memutar suara '{file_path}': {e}")
        else:
            # Jika nama suara tidak ditemukan dalam dictionary
            print(f"Sound '{sound_name}' tidak ditemukan di SoundManager.")
