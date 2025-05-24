import numpy as np
from PIL import Image, ImageSequence

def load_gif_frames(path):
    """
    Loads GIF frames from a specified path, converts them to RGBA,
    resizes to 60x60, and returns them as a list of NumPy arrays.
    """
    try:
        gif = Image.open(path)
        frames = []
        for frame in ImageSequence.Iterator(gif):
            # Convert to RGBA and resize for consistency
            frame = frame.convert("RGBA").resize((60, 60))
            frames.append(np.array(frame))
        return frames
    except FileNotFoundError:
        print(f"Error: GIF file not found at '{path}'")
        return []
    except Exception as e:
        print(f"Error loading GIF frames from '{path}': {e}")
        return []

def calculate_sum(landmark_list):
    """
    Calculates a sum based on the x-coordinates of specific MediaPipe pose landmarks.
    Used to detect overall body movement.
    """
    if landmark_list and len(landmark_list) > 24: # Ensure enough landmarks exist
        # Landmarks for shoulders, elbows, wrists, hips
        indices = [11, 12, 13, 14, 15, 16, 23, 24]
        return sum(landmark_list[i].x * 480 for i in indices if i < len(landmark_list))
    return 0

def is_visible(landmark_list):
    """
    Checks if key pose landmarks (shoulders) are sufficiently visible.
    Used to determine if the user is properly in frame.
    """
    if landmark_list and len(landmark_list) > 12: # Ensure landmarks for shoulders exist
        return (landmark_list[11].visibility > 0.7 and
                landmark_list[12].visibility > 0.7)
    return False

