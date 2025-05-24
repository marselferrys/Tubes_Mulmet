import pygame
import time
import os

class SoundManager:
    """
    Manages sound playback using Pygame mixer.
    """
    def __init__(self, assets_dir="."): # Accept assets_dir parameter
        pygame.mixer.init()
        # Ensure that the sound files exist
        self.sounds = {
            'green_light': os.path.join(assets_dir, 'greenLight.mp3'),
            'red_light': os.path.join(assets_dir, 'redLight.mp3'),
            'win': os.path.join(assets_dir, 'win.mp3'),
            'lose': os.path.join(assets_dir, 'lose.mp3')
        }

    def play_sound(self, sound_name):
        """
        Plays a specific sound by its name.
        """
        file_path = self.sounds.get(sound_name)
        if file_path:
            if not os.path.exists(file_path):
                print(f"Peringatan: File suara tidak ditemukan di '{file_path}'.")
                return

            try:
                sound = pygame.mixer.Sound(file_path)
                sound.play()
                # Wait for sound to finish playing if it's a short, critical sound
                # For background sounds, this loop might be removed
                while pygame.mixer.get_busy():
                    time.sleep(0.01)
            except pygame.error as e:
                print(f"Error playing sound '{file_path}': {e}")
        else:
            print(f"Sound '{sound_name}' not found in SoundManager.")

