# 🎼 Choralink

**Auto-arranger for Gospel Musicians**  
Upload your MIDI, audio, or sheet music. Select an instrument. Get an arrangement that just works.

---

# 📜 Choralink Commit Log: v2.0

## 🧠 Phase 2 Merge by GitGPT & Kaji

### ✅ Major Additions:
- Integrated core backend logic:
  - arrangement_generator.py 🌸
  - music_analyzer.py 🌸
- Added instrument_config.py for dropdown-ready abstraction
- CLI interface enhanced via run_choralink.py
- Frontend scaffold initiated (visual_score.jsx, css)
- Audio processing logic imported (real_time_processor, harmony_matcher)
- README.md updated with clear usage and vision
- dev_log.md tracking evolution, bloom points, and agentic hooks

### 📦 Directory Refactor:
- Unified structure under `/Choralink`
- /backend/, /frontend/, /audio_engine/, /docs/, /examples/, /notebooks/ scaffolded
- Marked bloom points in logic files for semantic growth

### 🎯 Project Intent:
> “Simple. Sacred. Sound.”
> For Gospel musicians seeking harmony without hurdles.

## ✨ Features

- 🎵 Analyze MIDI, MusicXML, and audio files
- 🎷 Auto-generate arrangements for any instrument
- 🎚️ Detect key, tempo, chords, SATB parts
- 📄 PDF sheet music support (coming soon via OCR)

---

## 🚀 Quick Start

```bash
git clone https://github.com/Clark-Wallace/Choralink.git
cd Choralink
pip install -r backend/requirements.txt
python backend/run_choralink.py --input examples/sample_gospel_input.mid --instrument saxophone
```

---

## 📂 Input Formats

| Format      | Supported | Notes |
|-------------|-----------|-------|
| MIDI (.mid) | ✅        | Fully supported |
| Audio (.wav/.mp3) | ✅  | Key + chord estimation |
| MusicXML (.musicxml/.mxl) | ✅ | Full symbolic score parsing |
| PDF (.pdf) | ⚠️ Planned | Via Audiveris OCR |

---

## 🧱 Repo Structure

```
Choralink/
├── backend/        # MIDI/audio/musicxml analysis + arrangement generator
├── frontend/       # Planned: Streamlit/Gradio UI
├── examples/       # Example input files
├── docs/           # Developer guides & logs
├── notebooks/      # Usage walkthroughs in Jupyter
```

