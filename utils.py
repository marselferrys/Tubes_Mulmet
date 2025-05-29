import numpy as np
from PIL import Image, ImageSequence

def load_gif_frames(path):
    """
    Memuat frame-frame dari file GIF yang diberikan, mengonversinya ke format RGBA,
    mengubah ukurannya menjadi 60x60 piksel, dan mengembalikannya sebagai list array NumPy.
    """
    try:
        gif = Image.open(path)  # Membuka file GIF
        frames = []
        for frame in ImageSequence.Iterator(gif):
            # Mengonversi setiap frame ke RGBA dan ubah ukurannya agar konsisten
            frame = frame.convert("RGBA").resize((60, 60))
            frames.append(np.array(frame))  # Ubah menjadi array NumPy dan simpan ke list
        return frames
    except FileNotFoundError:
        print(f"Error: GIF file tidak ditemukan di path '{path}'")
        return []
    except Exception as e:
        print(f"Error saat memuat frame dari GIF '{path}': {e}")
        return []

def calculate_sum(landmark_list):
    """
    Menghitung jumlah (sum) dari nilai x pada landmark tubuh tertentu
    (seperti bahu, siku, pergelangan tangan, dan pinggul) untuk mendeteksi gerakan tubuh.
    """
    if landmark_list and len(landmark_list) > 24:  # Pastikan jumlah landmark mencukupi
        # Indeks landmark untuk bagian tubuh penting (pose landmark MediaPipe)
        indices = [11, 12, 13, 14, 15, 16, 23, 24]
        # Mengalikan posisi x dengan lebar frame (480) untuk mendapatkan posisi dalam piksel
        return sum(landmark_list[i].x * 480 for i in indices if i < len(landmark_list))
    return 0

def is_visible(landmark_list):
    """
    Mengecek apakah landmark utama (bahu kiri dan kanan) terlihat dengan jelas
    berdasarkan nilai 'visibility'. Digunakan untuk memastikan pengguna berada dalam frame kamera.
    """
    if landmark_list and len(landmark_list) > 12:  # Pastikan landmark bahu tersedia
        return (landmark_list[11].visibility > 0.7 and  # Bahu kiri terlihat jelas
                landmark_list[12].visibility > 0.7)     # Bahu kanan terlihat jelas
    return False
