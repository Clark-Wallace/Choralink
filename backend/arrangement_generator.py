"""
Choralink Arrangement Generator Module

This module provides functionality for generating instrument-specific arrangements
based on the analysis of choir music (MIDI or audio).
"""

import music21
from backend.music_analyzer import MusicAnalyzer
from typing import Dict, Optional, Any
from backend.modules.melody_extractor import extract_melody
from backend.modules.ai_composer import generate_melodic_line
from backend.modules.instrument_profile import get_instrument_profile
from backend.modules.arrangement_strategy import assign_instrument_role, score_phrase, simplify_phrase

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
        
    def generate_arrangement(self, input_file: str, instrument: str = "saxophone", target_key: Optional[str] = None, difficulty_level: str = "intermediate") -> Dict[str, Any]:
        """
        Generate an arrangement for the specified instrument based on the input file.
        
        Args:
            input_file: Path to the input music file (MIDI or audio)
            instrument: Name of the target instrument (e.g., "saxophone", "trumpet")
            target_key: Desired key for the arrangement (e.g., "Bb", "C"). If None, uses the original key.
            difficulty_level: Skill level for the arrangement ("beginner", "intermediate", "advanced", "virtuoso")
            
        Returns:
            Dictionary containing the generated music21 score object, MusicXML string,
            MIDI file path, and the original analysis results.
        """
        try:
            # Determine file type and analyze
            if input_file.lower().endswith(('.mid', '.midi', '.mxl', '.xml', '.musicxml')):
                analysis = self.analyzer.analyze_midi(input_file)
                is_midi = True
            elif input_file.lower().endswith(('.wav', '.mp3', '.aac', '.flac')):
                analysis = self.analyzer.analyze_audio(input_file)
                is_midi = False
            else:
                raise ValueError("Unsupported input file format. Please use MIDI, MusicXML, or common audio formats.")
            
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
            melody_extracted = False
            
            if is_midi:
                # Use the melody extractor for all MIDI/MusicXML files
                try:
                    melody_part = extract_melody(input_file)
                    
                    if melody_part and len(melody_part.flatten().notes) > 0:
                        # Transpose if needed
                        if interval:
                            melody_part = melody_part.transpose(interval)
                        
                        # Determine the instrument's role based on context
                        score_context = {
                            "style": "gospel",  # Default style
                            "section": "verse",  # Default section
                            "tempo": analysis.get("tempo", 120),
                            "density": 0.5,  # Could be calculated from score
                            "measure_index": 0  # Could track actual measure
                        }
                        
                        role = assign_instrument_role(instrument, score_context)
                        print(f"🎼 Assigned role '{role}' to {instrument}")
                        
                        # Get instrument profile
                        instrument_profile = get_instrument_profile(instrument)
                        
                        # Extract harmony grid from analysis
                        harmony_grid = analysis.get("chord_progression", ["C", "F", "G", "C"])
                        
                        # Generate part based on assigned role
                        if role == "lead":
                            # For lead instruments, try AI composer first
                            if "sax" in instrument.lower() or "trumpet" in instrument.lower():
                                try:
                                    # Generate lead line with AI composer
                                    composed_line = generate_melodic_line(
                                        harmony_grid=harmony_grid,
                                        instrument_profile=instrument_profile,
                                        style="gospel",
                                        emotion="grateful"
                                    )
                                    
                                    # Use the composed line if successful
                                    if composed_line and len(composed_line.flatten().notes) > 0:
                                        print(f"🎷 Using AI-composed {instrument} line")
                                        melody_part = composed_line
                                    else:
                                        print("⚠️ Composer fallback: using extracted melody.")
                                except Exception as e:
                                    print(f"⚠️ AI composer error: {e}. Using extracted melody.")
                                    
                        elif role == "harmony":
                            # For harmony role, create sustained notes on chord roots
                            harmony_part = music21.stream.Part()
                            current_offset = 0.0
                            for chord_name in harmony_grid:
                                try:
                                    # Create whole note on chord root
                                    root_pitch = chord_name[0]
                                    if root_pitch in 'ABCDEFG':
                                        n = music21.note.Note(root_pitch + "4")
                                        n.duration = music21.duration.Duration("whole")
                                        if interval:
                                            n = n.transpose(interval)
                                        harmony_part.insert(current_offset, n)
                                        current_offset += 4.0
                                except:
                                    pass
                            if len(harmony_part.flatten().notes) > 0:
                                melody_part = harmony_part
                                print(f"🎵 Generated harmony part for {instrument}")
                                
                        elif role == "echo":
                            # For echo role, delay and simplify the melody
                            if melody_part and len(melody_part.flatten().notes) > 2:
                                echo_part = music21.stream.Part()
                                # Skip first few notes and echo the rest
                                for i, note in enumerate(melody_part.flatten().notes[2:]):
                                    echo_note = music21.note.Note(note.pitch)
                                    echo_note.duration = note.duration
                                    echo_note.volume = music21.volume.Volume(velocity=int(note.volume.velocity * 0.7) if note.volume else 64)
                                    echo_note.volume.velocity = int(note.volume.velocity * 0.7)  # Softer
                                    echo_part.append(echo_note)
                                melody_part = echo_part
                                print(f"🔊 Generated echo part for {instrument}")
                                
                        elif role == "interjector":
                            # For interjector role, create brief bursts
                            interjection_part = music21.stream.Part()
                            # Add short riffs at phrase boundaries
                            for i in range(0, 16, 4):  # Every 4 measures
                                if i % 8 == 4:  # Alternate pattern
                                    # Create a short ascending riff
                                    for j, pitch_interval in enumerate([0, 2, 4]):
                                        n = music21.note.Note(60 + pitch_interval)
                                        n.duration = music21.duration.Duration(0.25)
                                        if interval:
                                            n = n.transpose(interval)
                                        interjection_part.insert(i + j * 0.25, n)
                            if len(interjection_part.flatten().notes) > 0:
                                melody_part = interjection_part
                                print(f"💥 Generated interjection part for {instrument}")
                        
                        # Apply difficulty-based simplification if needed
                        if difficulty_level in ["beginner", "intermediate"]:
                            # Score the phrase difficulty
                            notes_list = list(melody_part.flatten().notes)
                            if notes_list:
                                phrase_score = score_phrase(notes_list, instrument_profile)
                                
                                # Get difficulty thresholds
                                from backend.modules.arrangement_strategy import DIFFICULTY_THRESHOLDS
                                min_score, max_score = DIFFICULTY_THRESHOLDS.get(difficulty_level, (0, 10))
                                
                                # Simplify if too difficult
                                if phrase_score > max_score:
                                    print(f"📊 Phrase difficulty ({phrase_score:.1f}) exceeds {difficulty_level} level ({max_score})")
                                    simplified_notes = simplify_phrase(notes_list, difficulty_level)
                                    
                                    # Rebuild the melody part with simplified notes
                                    simplified_part = music21.stream.Part()
                                    for n in simplified_notes:
                                        simplified_part.append(n)
                                    melody_part = simplified_part
                                    print(f"✨ Simplified arrangement for {difficulty_level} level")
                        
                        # Add notes and rests to the instrument part
                        for element in melody_part.flatten().notesAndRests:
                            instrument_part.append(element)
                        melody_extracted = True
                    else:
                        # Fallback to voice parts if melody extraction fails
                        if analysis.get("voice_parts"):
                            # Prioritize soprano for melody instruments
                            voice_melody = analysis["voice_parts"].get("soprano")
                            if not voice_melody and analysis["voice_parts"]:
                                # Fallback to the first available part if soprano is missing
                                voice_melody = next(iter(analysis["voice_parts"].values()), None)
                            
                            if voice_melody:
                                # Transpose if needed
                                part_to_add = voice_melody.transpose(interval) if interval else voice_melody
                                
                                # Try to use AI composer for saxophone parts
                                if "sax" in instrument.lower():
                                    try:
                                        # Get instrument profile
                                        sax_profile = get_instrument_profile(instrument)
                                        
                                        # Extract harmony grid from analysis
                                        harmony_grid = analysis.get("chord_progression", ["C", "F", "G", "C"])
                                        
                                        # Generate saxophone line with AI composer
                                        composed_line = generate_melodic_line(
                                            harmony_grid=harmony_grid,
                                            instrument_profile=sax_profile,
                                            style="gospel",
                                            emotion="grateful"
                                        )
                                        
                                        # Use the composed line if successful
                                        if composed_line and len(composed_line.flatten().notes) > 0:
                                            print("🎷 Using AI-composed saxophone line")
                                            part_to_add = composed_line
                                        else:
                                            print("⚠️ Composer fallback: using extracted voice part.")
                                    except Exception as e:
                                        print(f"⚠️ AI composer error: {e}. Using extracted voice part.")
                                
                                # Add notes and rests to the instrument part
                                for element in part_to_add.flatten().notesAndRests:
                                    instrument_part.append(element)
                                melody_extracted = True
                except Exception as e:
                    print(f"Melody extraction failed: {e}. Falling back to chord-based generation.")
            
            # If no melody was extracted or input is audio, use enhanced fallback
            if not melody_extracted:
                print("🎵 No melody extracted, using fallback generation")
                
                # Get instrument profile if not already loaded
                if 'instrument_profile' not in locals():
                    instrument_profile = get_instrument_profile(instrument)
                
                # Get harmony grid
                harmony_grid = analysis.get("chord_progression", ["C", "F", "G", "C"])
                
                # Generate fallback melody
                fallback_part = self._generate_fallback_melody(harmony_grid, instrument_profile, interval)
                
                # Apply difficulty-based simplification to fallback
                if difficulty_level in ["beginner", "intermediate"]:
                    notes_list = list(fallback_part.flatten().notes)
                    if notes_list:
                        phrase_score = score_phrase(notes_list, instrument_profile)
                        from backend.modules.arrangement_strategy import DIFFICULTY_THRESHOLDS
                        min_score, max_score = DIFFICULTY_THRESHOLDS.get(difficulty_level, (0, 10))
                        
                        if phrase_score > max_score:
                            simplified_notes = simplify_phrase(notes_list, difficulty_level)
                            fallback_part = music21.stream.Part()
                            for n in simplified_notes:
                                fallback_part.append(n)
                
                # Add fallback notes to instrument part
                for element in fallback_part.flatten().notesAndRests:
                    instrument_part.append(element)
            
            score.insert(0, instrument_part)
            
            # Generate output files
            musicxml_output = score.write("musicxml")
            # Get the base filename without extension
            import os
            base_name = os.path.splitext(input_file)[0]
            midi_output_path = f"{base_name}_{instrument}_arrangement.mid"
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

    def _generate_fallback_melody(self, harmony_grid: list, instrument_profile: dict, interval=None) -> music21.stream.Part:
        """
        Generate a simple fallback melody based on chord progression.
        Used when all other methods fail.
        """
        fallback_part = music21.stream.Part()
        current_offset = 0.0
        
        # Use a simple pattern: root, fifth, third, root
        pattern = [0, 7, 4, 0]  # Intervals from root
        
        for chord_name in harmony_grid[:8]:  # Limit to 8 chords for safety
            try:
                # Extract root note
                root_name = chord_name[0] if chord_name and chord_name[0] in 'ABCDEFG' else 'C'
                
                for interval_step in pattern:
                    # Create note at appropriate pitch
                    pitch_midi = 60 + interval_step  # Start from middle C
                    
                    # Ensure within instrument range
                    if pitch_midi < instrument_profile["range"][0]:
                        pitch_midi = instrument_profile["range"][0]
                    elif pitch_midi > instrument_profile["range"][1]:
                        pitch_midi = instrument_profile["range"][1]
                    
                    n = music21.note.Note(pitch_midi)
                    n.duration = music21.duration.Duration(0.5)  # Eighth notes
                    
                    # Transpose if needed
                    if interval:
                        n = n.transpose(interval)
                    
                    fallback_part.insert(current_offset, n)
                    current_offset += 0.5
            except:
                # If anything fails, add a rest
                rest = music21.note.Rest(quarterLength=2.0)
                fallback_part.insert(current_offset, rest)
                current_offset += 2.0
                
        return fallback_part
    
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
