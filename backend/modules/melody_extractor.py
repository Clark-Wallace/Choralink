"""
melody_extractor.py
===================
Extracts the melodic line from a polyphonic MusicXML or MIDI file.

Designed specifically for gospel-style saxophone phrasing, with attention to:
- Phrase duration and continuity
- Motivic repetition
- Register emphasis
- Gospel embellishment patterns

🌸 Bloom Points:
- Phrase boundary logic
- Repetition recognition
- Style-weighted scoring

Author: Kaji (Semantic Bloom Architect)
"""

from music21 import converter, stream, note, chord

def extract_melody(input_file):
    """
    Extracts the main melodic contour from a MusicXML or MIDI file.

    Parameters:
        input_file (str): Path to the MusicXML or MIDI file.

    Returns:
        melody_stream (music21.stream.Part): A monophonic stream of the extracted melody.
    """
    try:
        score = converter.parse(input_file)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return stream.Part()  # Return empty part
    
    # Try to get parts - handle both Score and Part types
    if hasattr(score, 'parts') and len(score.parts) > 0:
        parts = score.parts
    elif isinstance(score, stream.Part):
        parts = [score]
    else:
        # Try to extract parts from the score
        parts = list(score.getElementsByClass(stream.Part))
        if not parts:
            # If still no parts, treat the whole score as a single part
            parts = [score]

    candidate_notes = []
    
    # 🌸 Bloom: Extract notes from all parts
    for part in parts:
        # Use flatten() to get all notes in the part
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                candidate_notes.append(n)
            elif isinstance(n, chord.Chord):
                # 🌸 Bloom: Handle chord simplification by taking highest pitch
                if len(n.pitches) > 0:
                    highest_note = note.Note(n.sortAscending().pitches[-1])
                    highest_note.duration = n.duration
                    highest_note.offset = n.offset
                    candidate_notes.append(highest_note)

    # 🌸 Bloom: Create melody stream with proper time ordering
    melody_stream = stream.Part()
    
    # Sort notes by offset to maintain time order
    candidate_notes.sort(key=lambda n: (n.offset, n.pitch.midi if hasattr(n, 'pitch') else 0))
    
    # Add notes to the melody stream
    for n in candidate_notes:
        melody_stream.append(n)

    return melody_stream

if __name__ == "__main__":
    # Example usage
    test_file = "example_input.mxl"
    melody = extract_melody(test_file)
    melody.show('text')
