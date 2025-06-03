# 🎵 Choralink Examples

This directory contains sample music files for testing Choralink's arrangement capabilities.

## 📁 Sample Files

### `ave_maria_sample.mid`
- **Format**: MIDI
- **Source**: Ave Maria by Schubert (solo piano arrangement)
- **Best for**: Testing melody extraction from classical pieces
- **Suggested use**:
  ```bash
  python3 backend/run_choralink.py --input examples/ave_maria_sample.mid --instrument saxophone
  ```

### `ave_maria_sample.xml`
- **Format**: MusicXML
- **Source**: Same as above, in XML format
- **Best for**: Testing MusicXML parsing and score analysis
- **Suggested use**:
  ```bash
  python3 backend/run_choralink.py --input examples/ave_maria_sample.xml --instrument trumpet --difficulty beginner
  ```

### `gospel_progression_sample.mid`
- **Format**: MIDI
- **Source**: Original gospel chord progression (C-Am-F-G)
- **Best for**: Testing gospel-style arrangements and AI composition
- **Suggested use**:
  ```bash
  python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument saxophone --difficulty intermediate
  ```

## 🧪 Quick Test Commands

### Test Different Instruments
```bash
# Saxophone (lead role)
python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument saxophone

# Trumpet (echo/interjector role)  
python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument trumpet

# Flute (echo role)
python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument flute
```

### Test Difficulty Levels
```bash
# Beginner - simplified rhythms and range
python3 backend/run_choralink.py --input examples/ave_maria_sample.xml --instrument saxophone --difficulty beginner

# Advanced - full complexity
python3 backend/run_choralink.py --input examples/ave_maria_sample.xml --instrument saxophone --difficulty advanced
```

### Test Transposition
```bash
# Transpose for Bb instruments
python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument "tenor saxophone" --key Bb

# Transpose for Eb instruments  
python3 backend/run_choralink.py --input examples/gospel_progression_sample.mid --instrument "alto saxophone" --key Eb
```

## 📤 Output Files

After running arrangements, you'll find new MIDI files in this directory with names like:
- `gospel_progression_sample_saxophone_arrangement.mid`
- `ave_maria_sample_trumpet_arrangement.mid`

These can be:
- Imported into notation software (MuseScore, Finale, Sibelius)
- Used in DAWs for playback and editing
- Shared with musicians as practice tracks

## 🎼 Adding Your Own Files

To test with your own music:

1. **MIDI files** (.mid, .midi) - Direct upload
2. **MusicXML files** (.xml, .mxl, .musicxml) - From notation software exports
3. **Audio files** (.wav, .mp3, .flac) - Limited analysis (key/tempo only)

Place them in this directory and reference them in commands:
```bash
python3 backend/run_choralink.py --input examples/your_song.mid --instrument piano
```

## 🚨 Cleanup

The output files are temporary. To clean up generated arrangements:
```bash
rm examples/*_arrangement*.mid
```