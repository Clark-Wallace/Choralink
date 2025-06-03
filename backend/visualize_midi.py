#!/usr/bin/env python3
"""
MIDI Visualization Script for detailed analysis
"""

import music21
import matplotlib.pyplot as plt
import numpy as np

def visualize_midi(midi_path):
    """Create visualizations of the MIDI file"""
    
    # Load the MIDI file
    score = music21.converter.parse(midi_path)
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Ave Maria Saxophone Arrangement Analysis', fontsize=16)
    
    # Get the first part (saxophone)
    part = score.parts[0]
    notes = part.flatten().notes
    
    # 1. Piano roll visualization
    ax1 = axes[0]
    note_data = []
    for n in notes:
        if isinstance(n, music21.note.Note):
            note_data.append({
                'pitch': n.pitch.midi,
                'start': n.offset,
                'duration': n.duration.quarterLength,
                'velocity': n.volume.velocity if n.volume.velocity else 64
            })
    
    if note_data:
        for note in note_data:
            ax1.barh(note['pitch'], note['duration'], 
                    left=note['start'], height=0.8,
                    alpha=note['velocity']/127.0,
                    color='steelblue', edgecolor='black')
        
        ax1.set_xlabel('Time (quarter notes)')
        ax1.set_ylabel('MIDI Pitch')
        ax1.set_title('Piano Roll View')
        ax1.grid(True, alpha=0.3)
        
        # Add saxophone range lines
        ax1.axhline(y=51, color='green', linestyle='--', alpha=0.5, label='Alto Sax Low (Eb3)')
        ax1.axhline(y=81, color='red', linestyle='--', alpha=0.5, label='Alto Sax High (A5)')
        ax1.legend()
    
    # 2. Pitch contour over time
    ax2 = axes[1]
    if note_data:
        times = [n['start'] + n['duration']/2 for n in note_data]
        pitches = [n['pitch'] for n in note_data]
        
        ax2.plot(times, pitches, 'o-', linewidth=2, markersize=8)
        ax2.set_xlabel('Time (quarter notes)')
        ax2.set_ylabel('MIDI Pitch')
        ax2.set_title('Melodic Contour')
        ax2.grid(True, alpha=0.3)
        
        # Add pitch names
        for t, p in zip(times, pitches):
            pitch_name = music21.pitch.Pitch(p).nameWithOctave
            ax2.text(t, p+0.5, pitch_name, ha='center', fontsize=10)
    
    # 3. Duration and dynamics analysis
    ax3 = axes[2]
    if note_data:
        positions = range(len(note_data))
        durations = [n['duration'] for n in note_data]
        
        ax3.bar(positions, durations, color='coral', alpha=0.7)
        ax3.set_xlabel('Note Index')
        ax3.set_ylabel('Duration (quarter notes)')
        ax3.set_title('Note Durations')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add pitch labels
        for i, n in enumerate(note_data):
            pitch_name = music21.pitch.Pitch(n['pitch']).nameWithOctave
            ax3.text(i, 0.1, pitch_name, ha='center', rotation=45, fontsize=9)
    
    plt.tight_layout()
    
    # Save the visualization
    output_path = midi_path.replace('.mid', '_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    # Also create a musical notation view
    try:
        # Create a new score with just the first few measures for clarity
        excerpt = music21.stream.Score()
        part_excerpt = music21.stream.Part()
        
        # Add instrument
        sax = music21.instrument.Saxophone()
        part_excerpt.append(sax)
        
        # Add the notes
        for n in notes[:20]:  # First 20 notes
            part_excerpt.append(n)
        
        excerpt.append(part_excerpt)
        
        # Save as MusicXML for better notation software compatibility
        xml_path = midi_path.replace('.mid', '_excerpt.xml')
        excerpt.write('musicxml', fp=xml_path)
        print(f"MusicXML excerpt saved to: {xml_path}")
        
        # Try to create a simple text representation
        print("\nText representation of the melody:")
        print("=" * 50)
        measure_num = 1
        current_offset = 0
        
        for n in notes[:20]:
            if n.offset >= current_offset + 4:  # New measure (assuming 4/4)
                measure_num += 1
                current_offset += 4
                print()
            
            if isinstance(n, music21.note.Note):
                print(f"M{measure_num}: {n.pitch.nameWithOctave} ({n.duration.type})", end=" | ")
        
        print("\n")
        
    except Exception as e:
        print(f"Could not create notation view: {e}")

if __name__ == "__main__":
    midi_path = "/Users/MAC_AI/Library/Mobile Documents/com~apple~CloudDocs/1. Get this business/June01/Choralink/GITHUB/Choralink/examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg._saxophone_arrangement.mid"
    visualize_midi(midi_path)