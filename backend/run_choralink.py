import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.arrangement_generator import ArrangementGenerator

parser = argparse.ArgumentParser(description="Choralink: Gospel Auto-Arranger")
parser.add_argument('--input', type=str, required=True, help="Path to input file (MIDI, MusicXML, etc.)")
parser.add_argument('--instrument', type=str, required=True, help="Instrument name (e.g., saxophone)")
parser.add_argument('--key', type=str, default=None, help="Target key (e.g., Bb)")
parser.add_argument('--difficulty', type=str, default="intermediate", 
                    choices=["beginner", "intermediate", "advanced", "virtuoso"],
                    help="Difficulty level for the arrangement")
parser.add_argument('--version', action='version', version='Choralink v0.5.0 (Phase 4 MVP)')

args = parser.parse_args()

generator = ArrangementGenerator()
result = generator.generate_arrangement(args.input, instrument=args.instrument, target_key=args.key, difficulty_level=args.difficulty)

if result.get("error"):
    print("❌ Error occurred while creating arrangement:")
    print(f"   {result['error']}")
    print("\n💡 Troubleshooting tips:")
    print("   • Make sure your input file is a valid MIDI, MusicXML, or audio file")
    print("   • Check that the file path doesn't contain special characters")
    print("   • Try a different input file to test the system")
    print("   • Run with --help to see all available options")
else:
    print("✅ Arrangement complete!")
    print(f"📁 MIDI file saved to: {result['midi_path']}")
    print(f"🎼 Assigned role: {getattr(result.get('analysis', {}), 'role', 'Unknown')}")
    print(f"🎵 Target instrument: {args.instrument}")
    if args.key:
        print(f"🎶 Transposed to: {args.key}")
    print(f"📊 Difficulty level: {args.difficulty}")
    print("\n💡 Next steps:")
    print("   • Import the MIDI file into notation software (MuseScore, Finale, etc.)")
    print("   • Or use it in your DAW for playback and editing")
    print("   • Try different instruments and difficulty levels for variety!")
