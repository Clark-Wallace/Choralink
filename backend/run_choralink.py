import argparse
from backend.arrangement_generator import ArrangementGenerator

parser = argparse.ArgumentParser(description="Choralink: Gospel Auto-Arranger")
parser.add_argument('--input', type=str, required=True, help="Path to input file (MIDI, MusicXML, etc.)")
parser.add_argument('--instrument', type=str, required=True, help="Instrument name (e.g., saxophone)")
parser.add_argument('--key', type=str, default=None, help="Target key (e.g., Bb)")

args = parser.parse_args()

generator = ArrangementGenerator()
result = generator.generate_arrangement(args.input, instrument=args.instrument, target_key=args.key)

if result.get("error"):
    print("❌ Error:", result["error"])
else:
    print("✅ Arrangement complete. MIDI saved to:", result["midi_path"])
