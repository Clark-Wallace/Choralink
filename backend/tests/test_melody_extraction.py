"""
Test script for melody extraction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from music21 import converter
from backend.modules.melody_extractor import extract_melody

def test_melody_extraction():
    """Test the melody extraction on the Ave Maria sample"""
    
    # Path to the test file
    test_file = "examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg._saxophone_arrangement_excerpt.xml"
    
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return
    
    print("Testing melody extraction on Ave Maria...")
    print("-" * 50)
    
    # Extract melody
    melody = extract_melody(test_file)
    
    # Print statistics
    notes = list(melody.flatten().notes)
    print(f"Total notes extracted: {len(notes)}")
    
    if notes:
        # Get pitch range
        pitches = [n.pitch.midi for n in notes if hasattr(n, 'pitch')]
        if pitches:
            print(f"Pitch range: {min(pitches)} to {max(pitches)} (MIDI numbers)")
            print(f"Pitch range: {notes[pitches.index(min(pitches))].pitch} to {notes[pitches.index(max(pitches))].pitch}")
        
        # Show first 10 notes
        print("\nFirst 10 notes of extracted melody:")
        for i, n in enumerate(notes[:10]):
            if hasattr(n, 'pitch'):
                print(f"  {i+1}. {n.pitch.nameWithOctave} (duration: {n.duration.quarterLength})")
        
        # Analyze for saxophone suitability
        print("\nSaxophone suitability analysis:")
        alto_sax_range = (49, 80)  # Db3 to Ab5 in MIDI numbers
        suitable_notes = sum(1 for p in pitches if alto_sax_range[0] <= p <= alto_sax_range[1])
        print(f"  Notes within alto saxophone range: {suitable_notes}/{len(pitches)} ({suitable_notes/len(pitches)*100:.1f}%)")
        
        # Save melody as MIDI for playback
        output_path = "test_extracted_melody.mid"
        melody.write('midi', fp=output_path)
        print(f"\nExtracted melody saved to: {output_path}")
    else:
        print("No notes found in extracted melody!")

if __name__ == "__main__":
    test_melody_extraction()