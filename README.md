# 🎼 Choralink

**AI-Powered Gospel Music Arrangement System**  
Transform your choir music into professional instrumental arrangements with intelligent role assignment and skill-appropriate complexity.

> "We are no longer arranging notes. We are giving breath to a voice."

---

## 🚀 What's New in v0.5.0 (Phase 4 MVP)

### 🎷 Intelligent Arrangement System
- **AI Composer Integration**: Original melodies generated based on harmonic context
- **Smart Role Assignment**: Instruments automatically assigned roles (Lead, Echo, Harmony, Interjector)
- **Skill-Based Filtering**: Four difficulty levels (beginner → virtuoso) with automatic simplification
- **Melody Extraction**: Intelligent extraction of melodic lines from polyphonic scores
- **Fallback Generation**: Robust system ensures playable output even with complex inputs

### 🎯 Key Features

- 🎵 **Multi-Format Support**: MIDI, MusicXML (.mxl, .xml), and audio files
- 🎷 **Instrument-Specific Arrangements**: Optimized for saxophone, trumpet, clarinet, flute, and more
- 🎼 **Context-Aware Generation**: Different arrangements for verse vs. chorus sections
- 📊 **Difficulty Adaptation**: Automatic complexity reduction for player skill levels
- 🔄 **Smart Transposition**: Automatic key adjustment for transposing instruments
- 🎺 **Gospel Idioms**: Built-in gospel-style phrasing and articulations

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Clark-Wallace/Choralink.git
cd Choralink
pip install -r backend/requirements.txt
```

### Basic Usage

```bash
# Simple arrangement
python backend/run_choralink.py --input song.mid --instrument saxophone

# With transposition and difficulty
python backend/run_choralink.py --input gospel_choir.xml --instrument trumpet --key Bb --difficulty beginner

# Show all options
python backend/run_choralink.py --help
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--input` | Input file path (required) | `choir_song.mxl` |
| `--instrument` | Target instrument (required) | `saxophone`, `trumpet`, `flute` |
| `--key` | Target key for transposition | `Bb`, `Eb`, `F` |
| `--difficulty` | Skill level | `beginner`, `intermediate`, `advanced`, `virtuoso` |

---

## 📂 Supported Formats

| Format | Status | Features |
|--------|--------|----------|
| MIDI (.mid, .midi) | ✅ Full | Complete analysis, voice extraction |
| MusicXML (.mxl, .xml, .musicxml) | ✅ Full | Score parsing, part detection |
| Audio (.wav, .mp3, .flac) | ✅ Basic | Key/tempo detection, chord analysis |
| PDF Sheet Music | 🔄 Planned | OCR via Audiveris integration |

---

## 🎭 Instrument Roles

The system intelligently assigns roles based on musical context:

| Role | Description | Example Instruments |
|------|-------------|-------------------|
| **Lead** | Primary melodic line | Saxophone, Trumpet |
| **Echo** | Delayed response patterns | Flute, Clarinet |
| **Harmony** | Sustained chord tones | Piano, Guitar, Bass |
| **Interjector** | Rhythmic punctuation | Trumpet (at phrase ends) |

---

## 🏗️ Architecture

```
Choralink/
├── backend/
│   ├── arrangement_generator.py    # Main orchestration engine
│   ├── music_analyzer.py          # MIDI/Audio analysis
│   ├── run_choralink.py          # CLI interface
│   └── modules/
│       ├── melody_extractor.py    # Melodic line extraction
│       ├── ai_composer.py         # AI melody generation
│       ├── instrument_profile.py  # Instrument characteristics
│       └── arrangement_strategy.py # Role assignment logic
├── frontend/                      # UI components (in development)
├── audio_engine/                  # Real-time processing
├── examples/                      # Sample files
├── docs/                         # Development logs
└── tests/                        # Test suites
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test arrangement strategies
python backend/tests/test_arrangement_strategy.py

# Test melody extraction
python backend/tests/test_melody_extraction.py
```

---

## 🎼 Example Workflows

### Gospel Choir to Saxophone Quartet
```bash
python backend/run_choralink.py --input choir_recording.mid --instrument "alto saxophone" --difficulty intermediate
python backend/run_choralink.py --input choir_recording.mid --instrument "tenor saxophone" --difficulty intermediate
python backend/run_choralink.py --input choir_recording.mid --instrument "baritone saxophone" --difficulty beginner
```

### Church Band Arrangement
```bash
python backend/run_choralink.py --input praise_song.xml --instrument trumpet --key Bb
python backend/run_choralink.py --input praise_song.xml --instrument piano --difficulty advanced
python backend/run_choralink.py --input praise_song.xml --instrument bass --difficulty intermediate
```

---

## 🤝 Contributing

We welcome contributions! Areas of focus:
- Gospel-specific articulation patterns
- Additional instrument profiles
- UI/Frontend development
- OCR integration for sheet music
- Real-time performance features

---

## 📈 Roadmap

### Current (v0.5.0)
- ✅ Phase 4 MVP Complete
- ✅ AI Composer Integration
- ✅ Intelligent Role Assignment
- ✅ Skill-Based Filtering

### Next Steps
- 🔄 Phase 3.4: Articulation Bloom Injection
- 🔄 Gospel embellishment patterns
- 🔄 Automatic breath mark insertion
- 🔄 Sheet music PDF generation
- 🔄 Web UI with Streamlit
- 🔄 Batch processing

---

## 📜 Development Log

See [docs/dev_log.md](docs/dev_log.md) for detailed development history and architectural decisions.

---

## 🙏 Acknowledgments

Built with love for the Gospel music community by the Choralink Team, with AI assistance from GitGPT, Kaji, and Claude.

> "Search the music. Don't fight the band."

---

## 📄 License

[License information to be added]

---

## 📞 Contact

[Contact information to be added]