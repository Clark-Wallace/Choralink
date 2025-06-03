#!/usr/bin/env python3
"""
Analyze the original MIDI file directly
"""

import music21
import mido

def analyze_with_mido(file_path):
    """Use mido library to analyze MIDI file"""
    print(f"Analyzing with mido: {file_path}")
    print("=" * 80)
    
    try:
        mid = mido.MidiFile(file_path)
        
        print(f"Type: {mid.type}")
        print(f"Ticks per beat: {mid.ticks_per_beat}")
        print(f"Number of tracks: {len(mid.tracks)}")
        
        for i, track in enumerate(mid.tracks):
            print(f"\nTrack {i}: {track.name}")
            print(f"Number of messages: {len(track)}")
            
            # Count message types
            note_ons = sum(1 for msg in track if msg.type == 'note_on' and msg.velocity > 0)
            note_offs = sum(1 for msg in track if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0))
            
            print(f"Note ONs: {note_ons}")
            print(f"Note OFFs: {note_offs}")
            
            # Get pitch range
            pitches = [msg.note for msg in track if msg.type == 'note_on' and msg.velocity > 0]
            if pitches:
                print(f"Pitch range: MIDI {min(pitches)} to {max(pitches)}")
                print(f"  Low: {music21.pitch.Pitch(midi=min(pitches))}")
                print(f"  High: {music21.pitch.Pitch(midi=max(pitches))}")
            
            # Show first few notes
            print("\nFirst 10 note events:")
            note_count = 0
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    pitch = music21.pitch.Pitch(midi=msg.note)
                    print(f"  {pitch.nameWithOctave} (vel={msg.velocity})")
                    note_count += 1
                    if note_count >= 10:
                        break
                        
    except Exception as e:
        print(f"Error with mido: {e}")

def analyze_with_music21_forced(file_path):
    """Force music21 to parse as MIDI"""
    print(f"\nAnalyzing with music21 (forced MIDI): {file_path}")
    print("=" * 80)
    
    try:
        # Force parsing as MIDI
        score = music21.converter.parse(file_path, format='midi')
        
        print(f"Number of parts: {len(score.parts)}")
        print(f"Total duration: {score.duration.quarterLength} quarter notes")
        
        for i, part in enumerate(score.parts):
            print(f"\nPart {i+1}:")
            notes = part.flatten().notes
            print(f"Total notes: {len(notes)}")
            
            if len(notes) > 0:
                # Show first 10 notes
                print("First 10 notes:")
                for j, n in enumerate(notes[:10]):
                    if isinstance(n, music21.note.Note):
                        print(f"  {n.pitch.nameWithOctave} ({n.duration.type})")
                    elif isinstance(n, music21.chord.Chord):
                        chord_notes = [p.nameWithOctave for p in n.pitches[:3]]
                        print(f"  Chord: [{', '.join(chord_notes)}] ({n.duration.type})")
                        
    except Exception as e:
        print(f"Error with music21: {e}")

if __name__ == "__main__":
    # First try mido
    try:
        import mido
        file_path = "/Users/MAC_AI/Library/Mobile Documents/com~apple~CloudDocs/1. Get this business/June01/Choralink/GITHUB/Choralink/examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg..mxl"
        analyze_with_mido(file_path)
    except ImportError:
        print("mido not installed, installing...")
        import subprocess
        subprocess.run(["pip3", "install", "mido"])
        import mido
        analyze_with_mido(file_path)
    
    # Then try music21 with forced MIDI format
    analyze_with_music21_forced(file_path)