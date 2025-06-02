"""
Choralink Music Analyzer Module

This module provides functionality for analyzing music files (MIDI and audio)
to extract key, tempo, chord progression, and voice parts.
"""

import music21
import librosa
import numpy as np
from typing import Dict, List, Optional, Union, Any


class MusicAnalyzer:
    """
    A class for analyzing music files and extracting musical features.
    
    This analyzer can process both MIDI and audio files to extract key, tempo,
    chord progression, and voice parts (SATB) information.
    """
    
    def __init__(self):
        """Initialize the MusicAnalyzer with default values."""
        self.key = None
        self.tempo = None
        self.time_signature = None
        
    def analyze_midi(self, midi_file: str) -> Dict[str, Any]:
        """
        Analyze a MIDI file to extract key, tempo, chord progression, and voice parts.
        
        Args:
            midi_file: Path to the MIDI file to analyze
            
        Returns:
            Dictionary containing analysis results including key, tempo, time signature,
            voice parts, and chord progression
        """
        try:
            score = music21.converter.parse(midi_file)
            
            # Extract key
            key_analysis = score.analyze('key')
            self.key = key_analysis
            
            # Extract tempo
            self.tempo = None
            for element in score.flat:
                if isinstance(element, music21.tempo.MetronomeMark):
                    self.tempo = element.number
                    break
            
            # Default tempo if none found
            if self.tempo is None:
                self.tempo = 120
            
            # Extract time signature
            self.time_signature = None
            for element in score.flat:
                if isinstance(element, music21.meter.TimeSignature):
                    self.time_signature = element
                    break
            
            # Default time signature if none found
            if self.time_signature is None:
                self.time_signature = music21.meter.TimeSignature('4/4')
            
            # Extract voice parts (SATB)
            voice_parts = {}
            for part in score.parts:
                part_name = part.partName.lower() if part.partName else ''
                if 'soprano' in part_name:
                    voice_parts['soprano'] = part
                elif 'alto' in part_name:
                    voice_parts['alto'] = part
                elif 'tenor' in part_name:
                    voice_parts['tenor'] = part
                elif 'bass' in part_name:
                    voice_parts['bass'] = part
            
            # If no labeled parts found, try to infer based on pitch ranges
            if not voice_parts and len(score.parts) >= 4:
                # Sort parts by average pitch height
                parts_by_height = sorted(
                    score.parts, 
                    key=lambda p: sum(n.pitch.midi for n in p.flat.notes if hasattr(n, 'pitch')) / 
                                 max(1, len([n for n in p.flat.notes if hasattr(n, 'pitch')]))
                )
                
                if len(parts_by_height) >= 4:
                    voice_parts['soprano'] = parts_by_height[-1]  # Highest part
                    voice_parts['alto'] = parts_by_height[-2]     # Second highest
                    voice_parts['tenor'] = parts_by_height[-3]    # Third highest
                    voice_parts['bass'] = parts_by_height[-4]     # Lowest part
            
            # Extract chord progression
            chord_progression = []
            chords = score.chordify()
            for chord in chords.flat.getElementsByClass('Chord'):
                chord_name = chord.commonName
                if chord_name and chord_name not in chord_progression:
                    chord_progression.append(chord_name)
            
            return {
                'key': self.key.tonicPitchNameWithCase,
                'mode': self.key.mode,
                'tempo': self.tempo,
                'time_signature': str(self.time_signature),
                'voice_parts': voice_parts,
                'chord_progression': chord_progression
            }
            
        except Exception as e:
            print(f"Error analyzing MIDI file: {e}")
            return {
                'key': 'C',
                'mode': 'major',
                'tempo': 120,
                'time_signature': '4/4',
                'voice_parts': {},
                'chord_progression': ['C', 'G', 'Am', 'F']  # Default progression
            }
    
    def analyze_audio(self, audio_file: str) -> Dict[str, Any]:
        """
        Analyze an audio file to extract key, tempo, and chord progression.
        
        Args:
            audio_file: Path to the audio file to analyze
            
        Returns:
            Dictionary containing analysis results including tempo, key estimate,
            and chord progression
        """
        try:
            y, sr = librosa.load(audio_file)
            
            # Extract tempo
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
            self.tempo = tempo
            
            # Extract key
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # Simplified key detection using chroma features
            # Sum the chroma features to get the total energy in each pitch class
            chroma_sum = np.sum(chroma, axis=1)
            
            # The pitch class with the highest energy is likely the key
            key_idx = np.argmax(chroma_sum)
            
            # Map index to key name
            key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            estimated_key = key_names[key_idx]
            
            # Determine mode (major/minor) - simplified approach
            # Compare relative major/minor energy distribution
            major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])  # Major scale template
            minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])  # Minor scale template
            
            # Rotate profiles to match the estimated key
            major_profile = np.roll(major_profile, key_idx)
            minor_profile = np.roll(minor_profile, key_idx)
            
            # Calculate correlation with each profile
            major_corr = np.corrcoef(chroma_sum, major_profile)[0, 1]
            minor_corr = np.corrcoef(chroma_sum, minor_profile)[0, 1]
            
            mode = 'major' if major_corr > minor_corr else 'minor'
            
            # Extract chord progression using chroma features
            # This is a simplified approach - in a real implementation, we would use
            # a more sophisticated chord detection algorithm
            
            # Segment the audio into frames
            frame_length = 4096  # Adjust as needed
            hop_length = 2048    # Adjust as needed
            
            # Compute chroma features for each frame
            chroma_frames = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
            
            # Define chord templates (simplified to major and minor)
            chord_templates = {}
            for root in range(12):
                # Major chord template (root, major third, perfect fifth)
                major_template = np.zeros(12)
                major_template[root] = 1
                major_template[(root + 4) % 12] = 1
                major_template[(root + 7) % 12] = 1
                chord_templates[f"{key_names[root]}"] = major_template
                
                # Minor chord template (root, minor third, perfect fifth)
                minor_template = np.zeros(12)
                minor_template[root] = 1
                minor_template[(root + 3) % 12] = 1
                minor_template[(root + 7) % 12] = 1
                chord_templates[f"{key_names[root]}m"] = minor_template
            
            # Detect chords for each frame
            chord_progression = []
            for frame in range(chroma_frames.shape[1]):
                frame_chroma = chroma_frames[:, frame]
                
                # Find best matching chord
                best_chord = None
                best_score = -np.inf
                
                for chord_name, template in chord_templates.items():
                    score = np.dot(frame_chroma, template)
                    if score > best_score:
                        best_score = score
                        best_chord = chord_name
                
                if best_chord and (not chord_progression or chord_progression[-1] != best_chord):
                    chord_progression.append(best_chord)
            
            # Limit to a reasonable number of chords
            if len(chord_progression) > 8:
                # Find the most common chords
                from collections import Counter
                common_chords = Counter(chord_progression).most_common(8)
                chord_progression = [chord for chord, _ in common_chords]
            
            return {
                'tempo': self.tempo,
                'key': estimated_key,
                'mode': mode,
                'chord_progression': chord_progression
            }
            
        except Exception as e:
            print(f"Error analyzing audio file: {e}")
            return {
                'tempo': 120,
                'key': 'C',
                'mode': 'major',
                'chord_progression': ['C', 'G', 'Am', 'F']  # Default progression
            }
    
    def detect_key(self, midi_file: Optional[str] = None, audio_file: Optional[str] = None) -> Dict[str, str]:
        """
        Detect the key of a music file.
        
        Args:
            midi_file: Path to a MIDI file (optional)
            audio_file: Path to an audio file (optional)
            
        Returns:
            Dictionary containing key and mode information
        """
        if midi_file:
            analysis = self.analyze_midi(midi_file)
            return {'key': analysis['key'], 'mode': analysis['mode']}
        elif audio_file:
            analysis = self.analyze_audio(audio_file)
            return {'key': analysis['key'], 'mode': analysis['mode']}
        else:
            return {'key': 'C', 'mode': 'major'}  # Default
    
    def detect_tempo(self, midi_file: Optional[str] = None, audio_file: Optional[str] = None) -> float:
        """
        Detect the tempo of a music file.
        
        Args:
            midi_file: Path to a MIDI file (optional)
            audio_file: Path to an audio file (optional)
            
        Returns:
            Tempo in BPM (beats per minute)
        """
        if midi_file:
            analysis = self.analyze_midi(midi_file)
            return analysis['tempo']
        elif audio_file:
            analysis = self.analyze_audio(audio_file)
            return analysis['tempo']
        else:
            return 120.0  # Default tempo
    
    def get_chord_progression(self, midi_file: Optional[str] = None, audio_file: Optional[str] = None) -> List[str]:
        """
        Get the chord progression from a music file.
        
        Args:
            midi_file: Path to a MIDI file (optional)
            audio_file: Path to an audio file (optional)
            
        Returns:
            List of chord names in the progression
        """
        if midi_file:
            analysis = self.analyze_midi(midi_file)
            return analysis['chord_progression']
        elif audio_file:
            analysis = self.analyze_audio(audio_file)
            return analysis['chord_progression']
        else:
            return ['C', 'G', 'Am', 'F']  # Default progression


if __name__ == "__main__":
    # Example usage
    analyzer = MusicAnalyzer()
    
    # Test with a MIDI file if available
    import os
    example_midi = "../examples/sample_gospel_input.mid"
    if os.path.exists(example_midi):
        print("Analyzing MIDI file...")
        midi_analysis = analyzer.analyze_midi(example_midi)
        print(f"Key: {midi_analysis['key']} {midi_analysis['mode']}")
        print(f"Tempo: {midi_analysis['tempo']} BPM")
        print(f"Time Signature: {midi_analysis['time_signature']}")
        print(f"Chord Progression: {midi_analysis['chord_progression']}")
    else:
        print(f"Example MIDI file not found: {example_midi}")
