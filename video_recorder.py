import cv2
import os
import numpy as np

class VideoRecorder:
    """
    Records game footage to an MP4 file using OpenCV.
    """
    def __init__(self, output_filename="game_result.mp4", fps=30, frame_size=(800, 880), output_dir="."): # Changed default fps to 30
        self.output_filename_base = output_filename
        self.output_dir = output_dir
        self.full_output_path = os.path.join(self.output_dir, self.output_filename_base) # Now directly uses final path
        self.fps = fps
        self.frame_size = frame_size
        self.writer = None
        self.is_recording = False

    def start_recording(self):
        """
        Initializes the video writer and starts recording.
        Ensures the output directory exists.
        """
        if self.writer is None:
            os.makedirs(self.output_dir, exist_ok=True)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(self.full_output_path, fourcc, self.fps, self.frame_size) # Write directly to final path
            
            if not self.writer.isOpened():
                print(f"ERROR: Tidak dapat membuka VideoWriter untuk {self.full_output_path}. Pastikan codec 'mp4v' tersedia.")
                print("Mencoba menggunakan codec 'XVID' sebagai alternatif...")
                fourcc_fallback = cv2.VideoWriter_fourcc(*'XVID')
                self.writer = cv2.VideoWriter(self.full_output_path, fourcc_fallback, self.fps, self.frame_size)
                if not self.writer.isOpened():
                    print("ERROR: Gagal membuka VideoWriter dengan 'XVID' juga. Perekaman video tidak akan berfungsi.")
                    return

            self.is_recording = True
            print(f"Mulai merekam video ke {self.full_output_path}...")
        else:
            print("Perekaman sudah berjalan.")

    def write_frame(self, frame_rgb):
        """
        Writes a single frame to the video file if recording is active.
        Converts the frame from RGB (Pygame format) to BGR (OpenCV format) before writing.
        """
        if self.is_recording and self.writer is not None:
            if frame_rgb.shape[0] == self.frame_size[1] and frame_rgb.shape[1] == self.frame_size[0]:
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                self.writer.write(frame_bgr)
            # else: # Suppress warning if it's just a minor occasional mismatch
            #     print(f"Peringatan: Ukuran frame ({frame_rgb.shape[1]}, {frame_rgb.shape[0]}) tidak cocok dengan ukuran perekam ({self.frame_size[0]}, {self.frame_size[1]}). Frame tidak direkam.")

    def stop_recording(self):
        """
        Releases the video writer and stops recording.
        The video file is now saved.
        """
        if self.is_recording and self.writer is not None:
            self.writer.release()
            self.writer = None
            self.is_recording = False
            print(f"Video disimpan sebagai {self.full_output_path}")
        elif not self.is_recording:
            print("Perekaman tidak aktif.")

    def is_active(self):
        """
        Checks if the recorder is currently active.
        """
        return self.is_recording

