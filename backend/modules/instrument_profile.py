"""
instrument_profile.py
====================
Defines instrument-specific characteristics and idioms for arrangement generation.

Each profile contains:
- Range (in MIDI numbers)
- Default pitch for fallback
- Phrasing characteristics
- Articulation preferences
- Gospel-specific idioms

🌸 Bloom Points:
- Breath marks and phrase boundaries
- Idiomatic patterns
- Range restrictions for playability

Author: Choralink Team
"""

INSTRUMENT_PROFILES = {
    "saxophone": {
        "range": (49, 87),  # Db3 to Eb6 (alto saxophone concert pitch)
        "default_pitch": 65,  # F4
        "phrasing": "breath-arc",
        "articulation": "slur",
        "gospel_idioms": ["bend", "growl", "subtone"],
        "typical_register": "middle",
        "transposition": -9  # Alto sax transposes down a major 6th
    },
    "trumpet": {
        "range": (52, 82),  # E3 to Bb5 (concert pitch)
        "default_pitch": 67,  # G4
        "phrasing": "fanfare",
        "articulation": "tongued",
        "gospel_idioms": ["shake", "fall", "doit"],
        "typical_register": "upper-middle",
        "transposition": -2  # Bb trumpet transposes down a major 2nd
    },
    "clarinet": {
        "range": (50, 90),  # D3 to F#6 (concert pitch)
        "default_pitch": 62,  # D4
        "phrasing": "legato-flow",
        "articulation": "smooth",
        "gospel_idioms": ["glissando", "flutter-tongue"],
        "typical_register": "middle",
        "transposition": -2  # Bb clarinet transposes down a major 2nd
    },
    "flute": {
        "range": (60, 96),  # C4 to C7
        "default_pitch": 72,  # C5
        "phrasing": "floating",
        "articulation": "light",
        "gospel_idioms": ["trill", "grace-note"],
        "typical_register": "upper",
        "transposition": 0  # Concert pitch
    }
}

def get_instrument_profile(instrument_name):
    """
    Get the profile for a specific instrument.
    
    Args:
        instrument_name (str): Name of the instrument
        
    Returns:
        dict: Instrument profile with characteristics
    """
    # Normalize the instrument name
    name_lower = instrument_name.lower()
    
    # Handle saxophone variants
    if "sax" in name_lower:
        if "alto" in name_lower:
            profile = INSTRUMENT_PROFILES["saxophone"].copy()
        elif "tenor" in name_lower:
            profile = INSTRUMENT_PROFILES["saxophone"].copy()
            profile["range"] = (44, 81)  # Ab2 to A5
            profile["transposition"] = -14  # Tenor sax transposes down a major 9th
        elif "soprano" in name_lower:
            profile = INSTRUMENT_PROFILES["saxophone"].copy()
            profile["range"] = (54, 94)  # F#3 to Bb6
            profile["transposition"] = -2  # Bb soprano sax
        elif "baritone" in name_lower:
            profile = INSTRUMENT_PROFILES["saxophone"].copy()
            profile["range"] = (36, 75)  # C2 to Eb5
            profile["transposition"] = -21  # Eb baritone sax
        else:
            profile = INSTRUMENT_PROFILES["saxophone"]
    else:
        # Return the profile if it exists, otherwise return a default
        profile = INSTRUMENT_PROFILES.get(name_lower, {
            "range": (48, 84),  # C3 to C6 - generic range
            "default_pitch": 60,  # Middle C
            "phrasing": "standard",
            "articulation": "normal",
            "gospel_idioms": [],
            "typical_register": "middle",
            "transposition": 0
        })
    
    return profile