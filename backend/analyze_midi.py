#!/usr/bin/env python3
"""
MIDI Analysis Script for Choralink
Analyzes MIDI files for saxophone arrangement suitability
"""

import music21
import os
import sys
from music21 import converter, stream, note, chord, tempo, meter

def analyze_midi(midi_path):
    """Analyze a MIDI file for saxophone arrangement"""
    
    print(f"Analyzing: {os.path.basename(midi_path)}")
    print("=" * 80)
    
    try:
        # Load the MIDI file
        score = converter.parse(midi_path)
        
        # Basic information
        print("\n1. BASIC SCORE INFORMATION")
        print(f"   Number of parts: {len(score.parts)}")
        print(f"   Total duration: {score.duration.quarterLength} quarter notes")
        
        # Analyze tempo
        tempos = score.flatten().getElementsByClass(tempo.MetronomeMark)
        if tempos:
            print(f"   Tempo: {tempos[0].number} BPM ({tempos[0].text if hasattr(tempos[0], 'text') else ''})")
        
        # Analyze time signature
        time_sigs = score.flatten().getElementsByClass(meter.TimeSignature)
        if time_sigs:
            print(f"   Time signature: {time_sigs[0]}")
        
        # Analyze each part
        for i, part in enumerate(score.parts):
            print(f"\n2. PART {i+1} ANALYSIS")
            
            # Instrument information
            print(f"   Part name: {part.partName if part.partName else 'Unnamed'}")
            instruments = part.getElementsByClass(music21.instrument.Instrument)
            if instruments:
                print(f"   Assigned instrument: {instruments[0]}")
                print(f"   MIDI Program: {instruments[0].midiProgram}")
            
            # Get all notes
            notes = part.flatten().notes
            print(f"   Total note events: {len(notes)}")
            
            if len(notes) > 0:
                # Separate notes and chords
                single_notes = [n for n in notes if isinstance(n, note.Note)]
                chords = [c for c in notes if isinstance(c, chord.Chord)]
                
                print(f"   Single notes: {len(single_notes)}")
                print(f"   Chords: {len(chords)}")
                
                # Get all pitches (including from chords)
                all_pitches = []
                for n in notes:
                    if isinstance(n, note.Note):
                        all_pitches.append(n.pitch)
                    elif isinstance(n, chord.Chord):
                        all_pitches.extend(n.pitches)
                
                if all_pitches:
                    # Pitch range analysis
                    lowest_pitch = min(all_pitches)
                    highest_pitch = max(all_pitches)
                    
                    print(f"\n3. PITCH RANGE ANALYSIS")
                    print(f"   Lowest note: {lowest_pitch} (MIDI {lowest_pitch.midi})")
                    print(f"   Highest note: {highest_pitch} (MIDI {highest_pitch.midi})")
                    print(f"   Range span: {highest_pitch.midi - lowest_pitch.midi} semitones")
                    
                    # Saxophone range comparison
                    print(f"\n4. SAXOPHONE RANGE COMPATIBILITY")
                    
                    # Alto sax ranges (most common for solo work)
                    alto_written_low = music21.pitch.Pitch('Bb3')
                    alto_written_high = music21.pitch.Pitch('F#6')
                    alto_concert_low = music21.pitch.Pitch('Db3')
                    alto_concert_high = music21.pitch.Pitch('A5')
                    
                    print(f"   Alto Sax Written Range: {alto_written_low} to {alto_written_high}")
                    print(f"   Alto Sax Concert Pitch: {alto_concert_low} to {alto_concert_high}")
                    
                    # Check if it fits
                    fits_concert = (lowest_pitch.midi >= alto_concert_low.midi and 
                                  highest_pitch.midi <= alto_concert_high.midi)
                    fits_written = (lowest_pitch.midi >= alto_written_low.midi and 
                                  highest_pitch.midi <= alto_written_high.midi)
                    
                    if fits_concert:
                        print(f"   ✓ Fits within alto saxophone concert pitch range")
                    elif fits_written:
                        print(f"   ✓ Fits within alto saxophone written range (already transposed)")
                    else:
                        print(f"   ⚠ Some notes outside comfortable saxophone range")
                        if lowest_pitch.midi < alto_concert_low.midi:
                            print(f"     - {alto_concert_low.midi - lowest_pitch.midi} semitones too low")
                        if highest_pitch.midi > alto_concert_high.midi:
                            print(f"     - {highest_pitch.midi - alto_concert_high.midi} semitones too high")
                
                # Key analysis
                print(f"\n5. KEY AND TONALITY ANALYSIS")
                key = part.analyze('key')
                print(f"   Detected key: {key}")
                print(f"   Key confidence: {key.correlationCoefficient:.2f}")
                
                # Melodic analysis
                print(f"\n6. MELODIC CHARACTERISTICS")
                
                # Note durations
                durations = [n.duration.quarterLength for n in single_notes]
                if durations:
                    print(f"   Shortest note: {min(durations)} quarters")
                    print(f"   Longest note: {max(durations)} quarters")
                    print(f"   Average duration: {sum(durations)/len(durations):.2f} quarters")
                
                # Interval analysis
                if len(single_notes) > 1:
                    intervals = []
                    for i in range(1, len(single_notes)):
                        interval = single_notes[i].pitch.midi - single_notes[i-1].pitch.midi
                        intervals.append(abs(interval))
                    
                    print(f"   Average interval leap: {sum(intervals)/len(intervals):.1f} semitones")
                    print(f"   Largest leap: {max(intervals)} semitones")
                    
                    # Count stepwise motion vs leaps
                    steps = sum(1 for i in intervals if i <= 2)
                    leaps = sum(1 for i in intervals if i > 2)
                    print(f"   Stepwise motion: {steps} ({steps/len(intervals)*100:.1f}%)")
                    print(f"   Leaps (>2 semitones): {leaps} ({leaps/len(intervals)*100:.1f}%)")
                
                # Show first few measures
                print(f"\n7. FIRST 8 MEASURES (TEXT REPRESENTATION)")
                measures = part.makeMeasures()
                for i, measure in enumerate(measures[:8]):
                    measure_notes = []
                    for n in measure.flatten().notes:
                        if isinstance(n, note.Note):
                            measure_notes.append(f"{n.pitch.nameWithOctave}({n.duration.quarterLength})")
                    if measure_notes:
                        print(f"   Measure {i+1}: {' '.join(measure_notes[:5])}" + 
                              (" ..." if len(measure_notes) > 5 else ""))
                
                # Overall assessment
                print(f"\n8. SAXOPHONE ARRANGEMENT ASSESSMENT")
                
                # Check various factors
                issues = []
                strengths = []
                
                # Range check
                if fits_concert or fits_written:
                    strengths.append("Range fits saxophone comfortably")
                else:
                    issues.append("Some notes outside optimal saxophone range")
                
                # Check for chords
                if len(chords) > 0:
                    issues.append(f"Contains {len(chords)} chords - saxophone is monophonic")
                else:
                    strengths.append("Monophonic line suitable for saxophone")
                
                # Check interval leaps
                if intervals and max(intervals) > 12:
                    issues.append(f"Contains large leaps ({max(intervals)} semitones)")
                
                # Check note durations for breathing
                if durations:
                    long_phrases = [d for d in durations if d > 4]
                    if long_phrases:
                        strengths.append("Contains sustained notes for expressive playing")
                
                print("\n   Strengths:")
                for s in strengths:
                    print(f"   ✓ {s}")
                
                if issues:
                    print("\n   Considerations:")
                    for issue in issues:
                        print(f"   ⚠ {issue}")
                
                print(f"\n   Overall: {'Good' if len(strengths) > len(issues) else 'Needs adaptation'} for saxophone arrangement")
                
    except Exception as e:
        print(f"Error analyzing MIDI file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Analyze the original file (which is actually a MIDI despite .mxl extension)
    original_path = "/Users/MAC_AI/Library/Mobile Documents/com~apple~CloudDocs/1. Get this business/June01/Choralink/GITHUB/Choralink/examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg..mxl"
    print("\n\n=== ANALYZING ORIGINAL FILE (PIANO ARRANGEMENT) ===\n")
    analyze_midi(original_path)
    
    print("\n\n=== ANALYZING SAXOPHONE ARRANGEMENT ===\n")
    midi_path = "/Users/MAC_AI/Library/Mobile Documents/com~apple~CloudDocs/1. Get this business/June01/Choralink/GITHUB/Choralink/examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg._saxophone_arrangement.mid"
    analyze_midi(midi_path)