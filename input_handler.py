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
        """
        Processes a single video frame to detect human pose.
        Returns the MediaPipe results.
        """
        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the image and find pose.
        results = self.pose.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, results):
        """
        Draws pose landmarks on the given frame.
        """
        if results.pose_landmarks:
            self.drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return frame

    def detect_movement(self, results, prev_hand_pos, threshold=15):
        """
        Detects significant hand movement based on MediaPipe landmarks.
        Returns (is_moving, current_hand_positions).
        """
        if results and results.pose_landmarks and len(results.pose_landmarks.landmark) > 16:
            landmarks = results.pose_landmarks.landmark
            current_left_hand_x = landmarks[15].x * 640 # Convert normalized to pixel
            current_right_hand_x = landmarks[16].x * 640 # Convert normalized to pixel

            if prev_hand_pos is None:
                return False, [current_left_hand_x, current_right_hand_x]

            left_movement = abs(current_left_hand_x - prev_hand_pos[0]) > threshold
            right_movement = abs(current_right_hand_x - prev_hand_pos[1]) > threshold

            return left_movement or right_movement, [current_left_hand_x, current_right_hand_x]
        return False, prev_hand_pos # Return prev_hand_pos if no landmarks

    def _butter_bandpass(self, lowcut, highcut, fs, order=5):
        """Helper to create Butterworth band-pass filter coefficients."""
        nyq = 0.5 * fs # Nyquist frequency
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def _butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        """Helper to apply the band-pass filter."""
        b, a = self._butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def get_user_voice_volume(self, lowcut=128.0, highcut=1024.0, fs=44100, order=5):
        """
        Records and processes sound to return its RMS volume within a frequency band.
        Returns the RMS value (float), not a boolean.
        """
        try:
            duration = 0.1 # Shorter duration for quicker response
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait() # Wait for the recording to complete

            # Ensure audio is 1D for filtering if it's 2D (channels)
            if audio.ndim > 1:
                audio_data = audio[:, 0]
            else:
                audio_data = audio

            filtered_audio = self._butter_bandpass_filter(audio_data, lowcut, highcut, fs, order=order)
            # Calculate RMS (Root Mean Square) for volume
            rms = np.sqrt(np.mean(filtered_audio**2))
            return rms # Return the actual RMS value
        except Exception as e:
            # This can happen if no audio device is available or other audio issues
            # print(f"Error recording audio: {e}") # Uncomment for debugging audio issues
            return 0.0 # Return 0.0 if there's an error or no sound input

