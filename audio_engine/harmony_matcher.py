"""
Choralink Harmony Matcher Module

This module provides functionality for matching harmony from audio input,
detecting chords, and supporting real-time music analysis.
"""

import librosa
import numpy as np
from typing import Dict, List, Optional, Union, Any
from collections import Counter


class HarmonyMatcher:
    """
    A class for matching harmony from audio input and detecting chords.
    
    This matcher can analyze audio in real-time or from files to identify
    chord progressions, keys, and other harmonic elements.
    """
    
    def __init__(self):
        """Initialize the HarmonyMatcher with chord templates."""
        self.chord_templates = self._create_chord_templates()
        
    def _create_chord_templates(self) -> Dict[str, np.ndarray]:
        """
        Create templates for common chord types.
        
        Returns:
            Dictionary mapping chord names to their chroma templates
        """
        # Major chords
        C_major = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])  # C, E, G
        # Minor chords
        C_minor = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0])  # C, Eb, G
        # Dominant 7th
        C_dom7 = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])   # C, E, G, Bb
        # Major 7th
        C_maj7 = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1])   # C, E, G, B
        
        templates = {
            'C': C_major, 'C#': np.roll(C_major, 1), 'D': np.roll(C_major, 2),
            'Eb': np.roll(C_major, 3), 'E': np.roll(C_major, 4), 'F': np.roll(C_major, 5),
            'F#': np.roll(C_major, 6), 'G': np.roll(C_major, 7), 'Ab': np.roll(C_major, 8),
            'A': np.roll(C_major, 9), 'Bb': np.roll(C_major, 10), 'B': np.roll(C_major, 11),
            'Cm': C_minor, 'C#m': np.roll(C_minor, 1), 'Dm': np.roll(C_minor, 2),
            'Ebm': np.roll(C_minor, 3), 'Em': np.roll(C_minor, 4), 'Fm': np.roll(C_minor, 5),
            'F#m': np.roll(C_minor, 6), 'Gm': np.roll(C_minor, 7), 'Abm': np.roll(C_minor, 8),
            'Am': np.roll(C_minor, 9), 'Bbm': np.roll(C_minor, 10), 'Bm': np.roll(C_minor, 11),
            'C7': C_dom7, 'C#7': np.roll(C_dom7, 1), 'D7': np.roll(C_dom7, 2),
            'Eb7': np.roll(C_dom7, 3), 'E7': np.roll(C_dom7, 4), 'F7': np.roll(C_dom7, 5),
            'F#7': np.roll(C_dom7, 6), 'G7': np.roll(C_dom7, 7), 'Ab7': np.roll(C_dom7, 8),
            'A7': np.roll(C_dom7, 9), 'Bb7': np.roll(C_dom7, 10), 'B7': np.roll(C_dom7, 11),
            'Cmaj7': C_maj7, 'C#maj7': np.roll(C_maj7, 1), 'Dmaj7': np.roll(C_maj7, 2),
            'Ebmaj7': np.roll(C_maj7, 3), 'Emaj7': np.roll(C_maj7, 4), 'Fmaj7': np.roll(C_maj7, 5),
            'F#maj7': np.roll(C_maj7, 6), 'Gmaj7': np.roll(C_maj7, 7), 'Abmaj7': np.roll(C_maj7, 8),
            'Amaj7': np.roll(C_maj7, 9), 'Bbmaj7': np.roll(C_maj7, 10), 'Bmaj7': np.roll(C_maj7, 11)
        }
        
        return templates
    
    def match_harmony(self, audio_file: str, frame_length: float = 0.5) -> List[str]:
        """
        Match harmony from an audio file.
        
        Args:
            audio_file: Path to the audio file
            frame_length: Length of each analysis frame in seconds
            
        Returns:
            List of chord names in the detected progression
        """
        try:
            y, sr = librosa.load(audio_file)
            
            # Extract chroma features
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # Segment audio into frames
            frame_samples = int(frame_length * sr)
            hop_length = frame_samples // 2  # 50% overlap
            
            # Compute chroma features for each frame
            chroma_frames = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
            
            # Detect chords for each frame
            frame_chords = []
            for frame in range(chroma_frames.shape[1]):
                frame_chroma = chroma_frames[:, frame]
                
                # Find best matching chord
                best_chord = self._find_best_chord(frame_chroma)
                frame_chords.append(best_chord)
            
            # Smooth the chord progression
            chord_progression = self._smooth_chord_progression(frame_chords)
            
            return chord_progression
            
        except Exception as e:
            print(f"Error matching harmony: {e}")
            return ['C', 'G', 'Am', 'F']  # Default progression
    
    def match_harmony_realtime(self, audio_buffer: bytes, sample_rate: int = 22050) -> str:
        """
        Match harmony from real-time audio buffer.
        
        Args:
            audio_buffer: Audio data as bytes
            sample_rate: Sample rate of the audio data
            
        Returns:
            Name of the detected chord
        """
        try:
            # Convert buffer to numpy array
            y = np.frombuffer(audio_buffer, dtype=np.float32)
            
            # Extract chroma features
            chroma = librosa.feature.chroma_cqt(y=y, sr=sample_rate)
            
            # Average chroma over the buffer
            mean_chroma = np.mean(chroma, axis=1)
            
            # Find best matching chord
            best_chord = self._find_best_chord(mean_chroma)
            
            return best_chord
            
        except Exception as e:
            print(f"Error matching real-time harmony: {e}")
            return 'C'  # Default chord
    
    def _find_best_chord(self, chroma_vector: np.ndarray) -> str:
        """
        Find the best matching chord for a chroma vector.
        
        Args:
            chroma_vector: 12-dimensional chroma feature vector
            
        Returns:
            Name of the best matching chord
        """
        best_chord = None
        best_score = -np.inf
        
        for chord_name, template in self.chord_templates.items():
            # Calculate correlation between chroma and chord template
            score = np.dot(chroma_vector, template)
            
            if score > best_score:
                best_score = score
                best_chord = chord_name
        
        return best_chord
    
    def _smooth_chord_progression(self, chord_sequence: List[str], window_size: int = 5) -> List[str]:
        """
        Smooth a chord sequence to remove noise and transient detections.
        
        Args:
            chord_sequence: List of detected chords
            window_size: Size of the smoothing window
            
        Returns:
            Smoothed chord progression
        """
        if len(chord_sequence) <= window_size:
            # If sequence is shorter than window, return most common chord
            counter = Counter(chord_sequence)
            return [counter.most_common(1)[0][0]]
        
        smoothed = []
        unique_chords = []
        
        # Use a sliding window approach
        for i in range(len(chord_sequence) - window_size + 1):
            window = chord_sequence[i:i+window_size]
            counter = Counter(window)
            most_common = counter.most_common(1)[0][0]
            
            if not smoothed or smoothed[-1] != most_common:
                smoothed.append(most_common)
                if most_common not in unique_chords:
                    unique_chords.append(most_common)
        
        return unique_chords
    
    def detect_key(self, audio_file: str) -> Dict[str, str]:
        """
        Detect the key of an audio file.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Dictionary containing key and mode information
        """
        try:
            y, sr = librosa.load(audio_file)
            
            # Extract chroma features
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # Sum the chroma features to get the total energy in each pitch class
            chroma_sum = np.sum(chroma, axis=1)
            
            # The pitch class with the highest energy is likely the key
            key_idx = np.argmax(chroma_sum)
            
            # Map index to key name
            key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            estimated_key = key_names[key_idx]
            
            # Determine mode (major/minor)
            major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])  # Major scale template
            minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])  # Minor scale template
            
            # Rotate profiles to match the estimated key
            major_profile = np.roll(major_profile, key_idx)
            minor_profile = np.roll(minor_profile, key_idx)
            
            # Calculate correlation with each profile
            major_corr = np.corrcoef(chroma_sum, major_profile)[0, 1]
            minor_corr = np.corrcoef(chroma_sum, minor_profile)[0, 1]
            
            mode = 'major' if major_corr > minor_corr else 'minor'
            
            return {'key': estimated_key, 'mode': mode}
            
        except Exception as e:
            print(f"Error detecting key: {e}")
            return {'key': 'C', 'mode': 'major'}  # Default
    
    def analyze_intensity(self, audio_file: str, frame_length: float = 1.0) -> List[float]:
        """
        Analyze the intensity/energy of an audio file over time.
        
        Args:
            audio_file: Path to the audio file
            frame_length: Length of each analysis frame in seconds
            
        Returns:
            List of intensity values (0.0-1.0) for each frame
        """
        try:
            y, sr = librosa.load(audio_file)
            
            # Compute RMS energy
            hop_length = int(frame_length * sr)
            rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
            
            # Normalize to 0-1 range
            if np.max(rms) > 0:
                intensity = rms / np.max(rms)
            else:
                intensity = rms
            
            return intensity.tolist()
            
        except Exception as e:
            print(f"Error analyzing intensity: {e}")
            return [0.5]  # Default medium intensity


if __name__ == "__main__":
    # Example usage
    matcher = HarmonyMatcher()
    
    # Test with an audio file if available
    import os
    example_audio = "../examples/sample_gospel_input.wav"
    if os.path.exists(example_audio):
        print("Matching harmony from audio file...")
        chord_progression = matcher.match_harmony(example_audio)
        print(f"Detected chord progression: {chord_progression}")
        
        key_info = matcher.detect_key(example_audio)
        print(f"Detected key: {key_info['key']} {key_info['mode']}")
        
        intensity = matcher.analyze_intensity(example_audio)
        print(f"Intensity profile (first 5 frames): {intensity[:5]}")
    else:
        print(f"Example audio file not found: {example_audio}")
