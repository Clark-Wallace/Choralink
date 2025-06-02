"""
Choralink Arrangement Generator Module

This module provides functionality for generating instrument-specific arrangements
based on the analysis of choir music (MIDI or audio).
"""

import music21
from backend.modules.music_analyzer import MusicAnalyzer
from typing import Dict, Optional, Any


class ArrangementGenerator:
    """
    A class for generating musical arrangements for specific instruments.
    
    This generator uses the MusicAnalyzer to understand the input music
    (key, tempo, chords, voice parts) and creates a new arrangement
    tailored for a chosen instrument, including transposition and part extraction.
    """
    
    def __init__(self):
        """Initialize the ArrangementGenerator with a MusicAnalyzer instance."""
        self.analyzer = MusicAnalyzer()
        
    def generate_arrangement(self, input_file: str, instrument: str = "saxophone", target_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate an arrangement for the specified instrument based on the input file.
        
        Args:
            input_file: Path to the input music file (MIDI or audio)
            instrument: Name of the target instrument (e.g., "saxophone", "trumpet")
            target_key: Desired key for the arrangement (e.g., "Bb", "C"). If None, uses the original key.
            
        Returns:
            Dictionary containing the generated music21 score object, MusicXML string,
            MIDI file path, and the original analysis results.
        """
        try:
            # Determine file type and analyze
            if input_file.lower().endswith(('.mid', '.midi')):
                analysis = self.analyzer.analyze_midi(input_file)
                is_midi = True
            elif input_file.lower().endswith(('.wav', '.mp3', '.aac', '.flac')):
                analysis = self.analyzer.analyze_audio(input_file)
                is_midi = False
            else:
                raise ValueError("Unsupported input file format. Please use MIDI or common audio formats.")
            
            # Create a new score for the instrument
            score = music21.stream.Score()
            instrument_part = music21.stream.Part()
            
            # Set instrument
            instrument_obj = self._get_music21_instrument(instrument)
            instrument_part.append(instrument_obj)
            
            # Set tempo and time signature from analysis
            if analysis.get("tempo"):
                instrument_part.append(music21.tempo.MetronomeMark(number=analysis["tempo"]))
            if analysis.get("time_signature"):
                # Parse time signature string
                try:
                    ts = music21.meter.TimeSignature(analysis["time_signature"].split(" ")[0]) # Handle '4/4 time' format
                    instrument_part.append(ts)
                except Exception:
                    instrument_part.append(music21.meter.TimeSignature("4/4")) # Default
            
            # Set key signature
            source_key_str = analysis.get("key", "C")
            source_mode = analysis.get("mode", "major")
            source_key = music21.key.Key(source_key_str, source_mode)
            instrument_part.append(source_key)
            
            # Determine transposition interval if target_key is specified
            interval = None
            if target_key and target_key != source_key_str:
                target_key_obj = music21.key.Key(target_key)
                interval = music21.interval.Interval(source_key.tonic, target_key_obj.tonic)
            
            # Extract and process musical content
            if is_midi and analysis.get("voice_parts"):
                # Prioritize soprano for melody instruments
                melody_part = analysis["voice_parts"].get("soprano")
                if not melody_part and analysis["voice_parts"]:
                    # Fallback to the first available part if soprano is missing
                    melody_part = next(iter(analysis["voice_parts"].values()), None)
                
                if melody_part:
                    # Transpose if needed
                    part_to_add = melody_part.transpose(interval) if interval else melody_part
                    
                    # Add notes and rests to the instrument part
                    for element in part_to_add.flat.notesAndRests:
                        instrument_part.append(element.clone())
            else:
                # If input is audio or MIDI without clear parts, generate based on chords/key
                # Placeholder: Generate a simple melody based on chord progression
                # In a real implementation, this would be more sophisticated
                current_offset = 0.0
                for chord_name in analysis.get("chord_progression", ["C"]):
                    try:
                        chord_obj = music21.harmony.ChordSymbol(chord_name)
                        root_note = chord_obj.root()
                        # Transpose root note if needed
                        if interval:
                            root_note = root_note.transpose(interval)
                        
                        # Add the root note with a default duration (e.g., whole note)
                        note = music21.note.Note(root_note.nameWithOctave)
                        note.duration = music21.duration.Duration("whole")
                        instrument_part.insert(current_offset, note)
                        current_offset += note.duration.quarterLength
                    except Exception as e:
                        print(f"Could not process chord {chord_name}: {e}")
                        # Add a rest if chord processing fails
                        rest = music21.note.Rest(type="whole")
                        instrument_part.insert(current_offset, rest)
                        current_offset += rest.duration.quarterLength
            
            score.insert(0, instrument_part)
            
            # Generate output files
            musicxml_output = score.write("musicxml")
            midi_output_path = input_file.replace(".mid", f"_{instrument}_arrangement.mid") \
                                      .replace(".midi", f"_{instrument}_arrangement.mid") \
                                      .replace(".wav", f"_{instrument}_arrangement.mid") \
                                      .replace(".mp3", f"_{instrument}_arrangement.mid")
            score.write("midi", fp=midi_output_path)
            
            return {
                "score": score,
                "musicxml": musicxml_output,
                "midi_path": midi_output_path,
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"Error generating arrangement: {e}")
            # Return a default empty arrangement or error indicator
            return {
                "score": music21.stream.Score(),
                "musicxml": None,
                "midi_path": None,
                "analysis": None,
                "error": str(e)
            }

    def _get_music21_instrument(self, instrument_name: str) -> music21.instrument.Instrument:
        """Maps an instrument name string to a music21 instrument object."""
        name_lower = instrument_name.lower()
        if "sax" in name_lower:
            if "alto" in name_lower:
                return music21.instrument.AltoSaxophone()
            elif "tenor" in name_lower:
                return music21.instrument.TenorSaxophone()
            elif "soprano" in name_lower:
                return music21.instrument.SopranoSaxophone()
            elif "baritone" in name_lower:
                return music21.instrument.BaritoneSaxophone()
            else:
                return music21.instrument.Saxophone() # Default Saxophone
        elif "trumpet" in name_lower:
            return music21.instrument.Trumpet()
        elif "clarinet" in name_lower:
            return music21.instrument.Clarinet()
        elif "flute" in name_lower:
            return music21.instrument.Flute()
        elif "violin" in name_lower:
            return music21.instrument.Violin()
        elif "viola" in name_lower:
            return music21.instrument.Viola()
        elif "cello" in name_lower:
            return music21.instrument.Violoncello()
        elif "piano" in name_lower:
            return music21.instrument.Piano()
        elif "guitar" in name_lower:
            return music21.instrument.Guitar()
        elif "bass" in name_lower:
             return music21.instrument.ElectricBass()
        # Add more instruments as needed
        else:
            print(f"Warning: Instrument 	'{instrument_name}	' not specifically mapped. Using generic Instrument.")
            return music21.instrument.Instrument() # Generic instrument


if __name__ == "__main__":
    # Example usage
    generator = ArrangementGenerator()
    
    # Test with a MIDI file if available
    import os
    example_midi = "../examples/sample_gospel_input.mid"
    if os.path.exists(example_midi):
        print("Generating arrangement for Saxophone...")
        arrangement_result = generator.generate_arrangement(example_midi, instrument="saxophone", target_key="Bb")
        
        if arrangement_result and not arrangement_result.get("error"):
            print(f"Arrangement generated successfully!")
            print(f"Analysis Key: {arrangement_result[	'analysis	'][	'key	']} {arrangement_result[	'analysis	'][	'mode	']}")
            print(f"Generated MIDI saved to: {arrangement_result[	'midi_path	']}")
            # Optionally show the score
            # arrangement_result['score'].show()
        else:
            print(f"Failed to generate arrangement: {arrangement_result.get('error')}")
    else:
        print(f"Example MIDI file not found: {example_midi}")
