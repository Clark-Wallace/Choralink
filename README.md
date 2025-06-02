# 🎶 Choralink

Choralink is an AI-assisted gospel music arrangement engine designed for accessibility, musicality, and intelligent growth. It helps musicians — especially gospel players — generate meaningful arrangements from MusicXML or MIDI files, with custom instrument support (e.g. saxophone).

---

## 🌟 Core Features

- 🎼 **Melody Extraction** — Identifies the most "singable" voice from a piano or SATB input
- 🎷 **Instrument-Aware Arrangement** — Adapts phrasing, dynamics, and range based on your selected instrument (starting with saxophone)
- 🧠 **Semantic Listening Logic** — Recognizes motifs, phrasing, and melodic intent
- 🎛️ **Simple UI Mode** (Coming soon via `choralink_ui.py`) — drag & drop, pick instrument, preview, export

---

## 📂 Directory Structure

```plaintext
Choralink/
├── backend/
│   ├── run_choralink.py
│   ├── arrangement_generator.py
│   ├── modules/
│   │   ├── melody_extractor.py
│   │   ├── instrument_profile.py
│   │   ├── arrangement_strategy.py
│   └── tests/
│       └── test_melody_extractor.py
├── examples/
│   └── sample_input.xml
├── dev_log.md
├── README.md
├── requirements.txt


python backend/run_choralink.py --input examples/sample_input.xml --instrument saxophone
