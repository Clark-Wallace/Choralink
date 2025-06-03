# 🎵 Choralink Quick Start Guide for Church Musicians

Welcome! This guide will help you get started with Choralink in under 5 minutes.

## 📋 Prerequisites

- Python 3.8 or higher installed on your computer
- Basic comfort with command line (we'll guide you!)

## 🚀 Step-by-Step Setup

### 1. Download Choralink

```bash
git clone https://github.com/Clark-Wallace/Choralink.git
cd Choralink
```

**Tip**: If you get a "command not found" error, you may need to install Git first.

### 2. Install Dependencies

```bash
python3 -m pip install -r backend/requirements.txt
```

**Common Issues**:
- If `python3` doesn't work, try just `python`
- On Windows, you might need to use `py -3` instead

### 3. Test with a Sample File

First, let's create a simple test:

```bash
# For Mac/Linux:
python3 backend/run_choralink.py --input examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg._saxophone_arrangement_excerpt.xml --instrument saxophone

# For Windows:
py -3 backend/run_choralink.py --input examples/Ave_Maria_D839_-_Schubert_-_Solo_Piano_Arrg._saxophone_arrangement_excerpt.xml --instrument saxophone
```

## 🎼 Common Use Cases

### Creating Parts for Your Praise Band

**Lead Instrument (Saxophone/Trumpet)**:
```bash
python3 backend/run_choralink.py --input your_song.mid --instrument saxophone --difficulty intermediate
```

**Support Instruments**:
```bash
python3 backend/run_choralink.py --input your_song.mid --instrument flute --difficulty beginner
```

### Adjusting for Player Skill Levels

- `--difficulty beginner`: Simplified rhythms, smaller range
- `--difficulty intermediate`: Standard arrangements
- `--difficulty advanced`: Full complexity
- `--difficulty virtuoso`: Challenging arrangements

## ❓ Troubleshooting

### "File not found" Error
- Make sure you're in the Choralink directory
- Use the full path to your file

### Deprecation Warnings
- These are normal and don't affect functionality
- We're working on updating the code

### Output Location
- MIDI files are saved in the same directory as your input file
- Look for `[filename]_[instrument]_arrangement.mid`

## 🎹 What to Do with Output Files

1. **Import to Notation Software**: 
   - Open the .mid file in MuseScore (free)
   - Or Finale/Sibelius (paid)
   
2. **Print Sheet Music**:
   - After importing to notation software
   - Export as PDF
   
3. **Create Practice Tracks**:
   - Import to your DAW
   - Add backing tracks

## 📧 Getting Help

- Check the full README for advanced features
- Report issues on GitHub
- Join our community (coming soon!)

## 🙏 Next Steps

1. Try different instruments and see how roles change
2. Experiment with difficulty levels
3. Process your church's repertoire
4. Share feedback to help us improve!

---

*Remember: Choralink is about making music accessible. Don't let technical hurdles stop you from creating beautiful arrangements for your congregation!*