import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter

class InputHandler:
    """
    Handles input from webcam (MediaPipe pose detection) and microphone (sound detection).
    """
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """Processes a single video frame to detect human pose."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, results):
        """Draws pose landmarks on the given frame."""
        if results.pose_landmarks:
            self.drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame

    def detect_movement(self, results, prev_hand_pos, threshold=15):
        """Detects significant hand movement based on MediaPipe landmarks."""
        if results and results.pose_landmarks and len(results.pose_landmarks.landmark) > 16:
            landmarks = results.pose_landmarks.landmark
            current_left_hand_x = landmarks[15].x * 640
            current_right_hand_x = landmarks[16].x * 640

            if prev_hand_pos is None:
                return False, [current_left_hand_x, current_right_hand_x]

            left_movement = abs(current_left_hand_x - prev_hand_pos[0]) > threshold
            right_movement = abs(current_right_hand_x - prev_hand_pos[1]) > threshold

            return left_movement or right_movement, [current_left_hand_x, current_right_hand_x]
        return False, prev_hand_pos

    def _butter_bandpass(self, lowcut, highcut, fs, order=5):
        """Creates Butterworth band-pass filter coefficients."""
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def _butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        """Applies the band-pass filter."""
        b, a = self._butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def detect_pitch_fft(self, audio_data, fs):
        """
        Detects dominant frequency in audio using FFT.
        """
        audio_data -= np.mean(audio_data)  # Remove DC offset
        window = np.hamming(len(audio_data))
        windowed_data = audio_data * window

        spectrum = np.fft.rfft(windowed_data)
        freqs = np.fft.rfftfreq(len(windowed_data), d=1.0/fs)
        magnitudes = np.abs(spectrum)

        peak_index = np.argmax(magnitudes)
        dominant_freq = freqs[peak_index]

        return dominant_freq

    def get_user_voice_volume_and_pitch(self, lowcut=128.0, highcut=1024.0, fs=44100, order=5):
        """
        Records and returns RMS volume and dominant frequency using FFT.
        """
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
