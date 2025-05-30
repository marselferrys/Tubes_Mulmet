#import modul eksternal yang diperlukan
import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter

class InputHandler:
    """
    kelas untuk menangani input video dan audio, mendeteksi pose manusia,
    """
    def __init__(self):
        # Inisialisasi MediaPipe Pose untuk mendeteksi pose manusia
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        # mengubah frame dari BGR ke RGB untuk MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, results):
        # menggambar landmark pose pada frame jika pose berhasil dideteksi
        if results.pose_landmarks:
            self.drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame

    def _butter_bandpass(self, lowcut, highcut, fs, order=5):
        # Membuat koefisien filter band-pass Butterworth, digunakan untuk menyaring frekuensi audio
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def _butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        # Menerapkan filter band-pass Butterworth pada data audio
        b, a = self._butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def detect_pitch_fft(self, audio_data, fs):
        # Menggunakan FFT untuk mendeteksi frekuensi dominan dari data audio.
        audio_data -= np.mean(audio_data)  
        window = np.hamming(len(audio_data))
        windowed_data = audio_data * window

        spectrum = np.fft.rfft(windowed_data)
        freqs = np.fft.rfftfreq(len(windowed_data), d=1.0/fs)
        magnitudes = np.abs(spectrum)

        peak_index = np.argmax(magnitudes)
        dominant_freq = freqs[peak_index]

        return dominant_freq

    def get_user_voice_volume_and_pitch(self, lowcut=128.0, highcut=1024.0, fs=44100, order=5):
        # Merekam suara pengguna dan menghitung volume serta pitch
        try:
            duration = 0.1  # 100 ms
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()

            audio_data = audio[:, 0] if audio.ndim > 1 else audio

            filtered_audio = self._butter_bandpass_filter(audio_data, lowcut, highcut, fs, order=order)
            rms = np.sqrt(np.mean(filtered_audio**2))
            pitch = self.detect_pitch_fft(filtered_audio, fs)

            return rms, pitch
        except Exception as e:
            return 0.0, 0.0
