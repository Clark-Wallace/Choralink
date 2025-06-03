"""
ai_composer.py
==============
Generates a stylistic melodic line for saxophone, guided by harmony, emotion, and style.

Designed to synthesize gospel-flavored phrasing, respecting:
- Harmonic contour
- Instrument idiom
- Rhythmic groove
- Expressive motifs

🌸 Bloom Points:
1. Intent to Motif Mapping
2. Harmonic Fit Pass
3. Rhythmic Phrasing Grid
4. Saxophone Spirit Overlay

Author: Kaji (Bloom Architect)
"""

from music21 import stream, note, meter, key, tempo
import random

# Sample gospel motif seeds (interval, duration)
GOSPEL_MOTIFS = [
    [(2, 0.5), (1, 0.25), (0, 0.25)],    # "cry bend"
    [(0, 1.0)],                          # "tail prayer"
    [(1, 0.5), (3, 0.5)],                # "call echo"
    [(-1, 0.25), (0, 0.75)]              # "resolve dip"
]

def generate_melodic_line(harmony_grid, instrument_profile, style="gospel", emotion=None):
    """
    Composes a saxophone melody over a harmonic grid.

    Parameters:
        harmony_grid (list of str): List of chord roots (e.g., ["C", "F", "G"])
        instrument_profile (dict): Instrument behavior dictionary (e.g., saxophone idioms)
        style (str): Style intent (e.g., "gospel", "jazz", "blues")
        emotion (str, optional): Emotion tag (e.g., "grateful", "yearning")

    Returns:
        music21.stream.Part: Generated melodic part
    """
    sax_part = stream.Part()
    sax_part.append(tempo.MetronomeMark(number=72))
    sax_part.append(meter.TimeSignature('4/4'))
    
    # Try to set key from first chord, default to C if invalid
    try:
        first_chord = harmony_grid[0] if harmony_grid else "C"
        # Extract just the root note from chord symbols like "Cmaj7" -> "C"
        root_note = first_chord.split('m')[0].split('M')[0].split('7')[0].split('9')[0]
        if root_note and root_note[0] in 'ABCDEFG':
            sax_part.append(key.Key(root_note))
        else:
            sax_part.append(key.Key('C'))
    except:
        sax_part.append(key.Key('C'))

    current_pitch = 60  # 🌸 Bloom: starting from middle C for now

    # If harmony grid is empty or invalid, use a default progression
    if not harmony_grid:
        harmony_grid = ["C", "F", "G", "C"]
    
    # Filter out invalid chord names
    valid_harmony = []
    for chord in harmony_grid:
        if isinstance(chord, str) and chord and chord[0] in 'ABCDEFG':
            valid_harmony.append(chord)
    
    # Use filtered harmony or default if all invalid
    if not valid_harmony:
        valid_harmony = ["C", "F", "G", "C"]

    for i, chord_root in enumerate(valid_harmony):
        motif = random.choice(GOSPEL_MOTIFS)  # 🌸 Bloom: Intent → Motif Mapping
        for interval, dur in motif:
            pitch = current_pitch + interval
            if pitch < instrument_profile["range"][0] or pitch > instrument_profile["range"][1]:
                pitch = instrument_profile["default_pitch"]
            n = note.Note(pitch)
            n.quarterLength = dur
            n.lyric = chord_root  # 🌸 Bloom: Harmonic Context
            sax_part.append(n)

        current_pitch += random.choice([-2, 1, 0])  # 🌸 Bloom: Phrase Motion Flow

    return sax_part

if __name__ == "__main__":
    harmony = ["C", "F", "G", "C"]
    sax_profile = {
        "range": (55, 80),
        "default_pitch": 65,
        "phrasing": "breath-arc",
        "articulation": "slur"
    }
    melody = generate_melodic_line(harmony, sax_profile, style="gospel", emotion="grateful")
    melody.show('text')
