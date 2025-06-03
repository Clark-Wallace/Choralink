#!/usr/bin/env python3
"""
Analyze the original MusicXML file
"""

import music21

def analyze_musicxml(file_path):
    """Analyze MusicXML file"""
    
    print(f"Analyzing MusicXML file: {file_path}")
    print("=" * 80)
    
    # Load the file
    score = music21.converter.parse(file_path)
    
    print(f"\nTotal parts: {len(score.parts)}")
    print(f"Total measures: {len(score.parts[0].getElementsByClass('Measure'))}")
    print(f"Total duration: {score.duration.quarterLength} quarter notes")
    
    # Analyze each part
    for i, part in enumerate(score.parts):
        print(f"\n--- PART {i+1}: {part.partName} ---")
        
        notes = part.flatten().notes
        print(f"Total note events: {len(notes)}")
        
        # Separate notes and chords
        single_notes = [n for n in notes if isinstance(n, music21.note.Note)]
        chords = [c for c in notes if isinstance(c, music21.chord.Chord)]
        
        print(f"Single notes: {len(single_notes)}")
        print(f"Chords: {len(chords)}")
        
        # Get pitch range
        all_pitches = []
        for n in notes:
            if isinstance(n, music21.note.Note):
                all_pitches.append(n.pitch)
            elif isinstance(n, music21.chord.Chord):
                all_pitches.extend(n.pitches)
        
        if all_pitches:
            lowest = min(all_pitches)
            highest = max(all_pitches)
            print(f"Pitch range: {lowest} to {highest}")
            print(f"Range span: {highest.midi - lowest.midi} semitones")
        
        # Show first few measures
        print("\nFirst 4 measures:")
        measures = part.getElementsByClass('Measure')
        for m_idx, measure in enumerate(measures[:4]):
            measure_notes = measure.flatten().notes
            note_str = []
            for n in measure_notes[:5]:  # First 5 notes per measure
                if isinstance(n, music21.note.Note):
                    note_str.append(f"{n.pitch.nameWithOctave}")
                elif isinstance(n, music21.chord.Chord):
                    note_str.append(f"[{','.join([p.nameWithOctave for p in n.pitches[:3]])}]")
            print(f"  M{m_idx+1}: {' '.join(note_str)}")

if __name__ == "__main__":
    file_path = "/Users/MAC_AI/Library/Mobile Documents/com~apple~CloudDocs/1. Get this business/June01/Choralink/GITHUB/Choralink/examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg..mxl"
    analyze_musicxml(file_path)