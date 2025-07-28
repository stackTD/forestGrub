# This file contains simple sound generation for the dinosaur game
# Due to environment limitations, we'll create placeholder sound functions

import pygame
import numpy as np

def generate_jump_sound():
    """Generate a simple jump sound effect"""
    try:
        duration = 0.2
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a simple frequency sweep for jump sound
        freq_start = 200
        freq_end = 400
        
        arr = np.zeros((frames, 2))
        for i in range(frames):
            freq = freq_start + (freq_end - freq_start) * (i / frames)
            wave = np.sin(2 * np.pi * freq * i / sample_rate)
            wave *= 0.3 * (1 - i / frames)  # Fade out
            arr[i] = [wave, wave]
        
        # Convert to pygame sound
        sound_array = np.array(arr * 32767, dtype=np.int16)
        return pygame.sndarray.make_sound(sound_array)
    except:
        return None

def generate_hit_sound():
    """Generate a simple hit/game over sound effect"""
    try:
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a simple low frequency for hit sound
        freq = 100
        
        arr = np.zeros((frames, 2))
        for i in range(frames):
            wave = np.sin(2 * np.pi * freq * i / sample_rate)
            wave *= 0.3 * (1 - i / frames)  # Fade out
            arr[i] = [wave, wave]
        
        # Convert to pygame sound
        sound_array = np.array(arr * 32767, dtype=np.int16)
        return pygame.sndarray.make_sound(sound_array)
    except:
        return None

def generate_point_sound():
    """Generate a simple point scoring sound effect"""
    try:
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Generate a simple high frequency beep
        freq = 800
        
        arr = np.zeros((frames, 2))
        for i in range(frames):
            wave = np.sin(2 * np.pi * freq * i / sample_rate)
            wave *= 0.2
            arr[i] = [wave, wave]
        
        # Convert to pygame sound
        sound_array = np.array(arr * 32767, dtype=np.int16)
        return pygame.sndarray.make_sound(sound_array)
    except:
        return None