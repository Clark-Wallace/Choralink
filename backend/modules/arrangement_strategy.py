"""
arrangement_strategy.py
=======================
Determines the appropriate musical role and simplification strategy for a saxophone line
based on skill level, instrument profile, and style.

Roles: Lead, Echo, Harmony, Interjector
Skill levels: Beginner, Intermediate, Advanced, Virtuoso

🌸 Bloom Points:
- Role assignment based on phrasing and style
- Phrase difficulty scoring
- Adaptive simplification if score exceeds skill threshold

Author: Kaji (Bloom Architect)
"""

DIFFICULTY_THRESHOLDS = {
    "beginner": (0, 3),
    "intermediate": (3, 6),
    "advanced": (6, 8),
    "virtuoso": (8, 10)
}

def score_phrase(phrase, instrument_profile):
    """
    Score a phrase on difficulty scale 0–10.

    Parameters:
        phrase (list of music21.note.Note): The phrase to score.
        instrument_profile (dict): Info about range, articulation needs, etc.

    Returns:
        float: Difficulty score from 0 to 10.
    """
    jumps = 0
    rhythm_complexity = 0
    ornament_count = 0
    breath_range = 0

    last_pitch = None
    for n in phrase:
        if last_pitch:
            interval_jump = abs(n.pitch.midi - last_pitch)
            jumps += interval_jump > 5
        rhythm_complexity += 1 if n.quarterLength < 0.5 else 0
        ornament_count += 1 if n.tie or n.articulations else 0
        last_pitch = n.pitch.midi

    phrase_len = len(phrase)
    breath_range = phrase_len > 8

    # Combine into score
    score = (
        jumps * 2 +
        rhythm_complexity * 1.5 +
        ornament_count * 2 +
        (2 if breath_range else 0)
    )
    return min(score, 10)

def simplify_phrase(phrase, target_level):
    """
    Simplify a phrase to match the player's skill level.

    Parameters:
        phrase (list of music21.note.Note): The original phrase.
        target_level (str): Skill level.

    Returns:
        list: Simplified phrase.
    """
    simplified = []
    for n in phrase:
        n.quarterLength = max(0.5, n.quarterLength)  # Slow down
        n.articulations = []  # Strip embellishments
        simplified.append(n)
    return simplified

def assign_role(measure_index, section, style_tag):
    """
    Assign musical role based on style and section.

    Returns:
        str: One of 'lead', 'echo', 'harmony', 'interjector'
    """
    if style_tag == "gospel":
        if section == "verse":
            return "lead" if measure_index % 2 == 0 else "echo"
        else:
            return "harmony"
    return "lead"

def assign_instrument_role(instrument_name, score_context):
    """
    Determines the appropriate role for an instrument based on context.
    
    Parameters:
        instrument_name (str): Name of the instrument (e.g., "saxophone", "trumpet")
        score_context (dict): Contains tempo, time_signature, density, style, section
        
    Returns:
        str: Role assignment ('lead', 'echo', 'harmony', 'interjector')
    """
    # Default roles based on instrument characteristics
    default_roles = {
        "saxophone": "lead",      # Saxophone excels at melodic lines
        "trumpet": "lead",        # Can lead or interject
        "clarinet": "harmony",    # Smooth for harmonic support
        "flute": "echo",         # Light, good for echoes
        "piano": "harmony",      # Natural harmonic instrument
        "bass": "harmony",       # Foundation support
        "guitar": "harmony"      # Chord support
    }
    
    # Normalize instrument name
    instrument_lower = instrument_name.lower()
    
    # Check for specific instrument types
    for key in default_roles:
        if key in instrument_lower:
            base_role = default_roles[key]
            break
    else:
        base_role = "lead"  # Default to lead if unknown
    
    # Get context parameters
    style = score_context.get("style", "gospel")
    section = score_context.get("section", "verse")
    density = score_context.get("density", 0.5)
    tempo = score_context.get("tempo", 120)
    measure_index = score_context.get("measure_index", 0)
    
    # Adjust role based on musical context
    if style == "gospel":
        if "sax" in instrument_lower:
            # Saxophone leads in verses, harmonizes in dense sections
            if section == "verse" and density < 0.7:
                return "lead"
            elif section == "chorus" and density > 0.7:
                return "harmony"
            elif measure_index % 4 == 3:  # Every 4th bar
                return "interjector"
            else:
                return "lead"
                
        elif "trumpet" in instrument_lower:
            # Trumpet interjects in gospel, especially at phrase ends
            if measure_index % 8 in [3, 7]:  # End of 4-bar phrases
                return "interjector"
            elif section == "bridge":
                return "lead"
            else:
                return "echo"
                
        elif "flute" in instrument_lower:
            # Flute provides ethereal echoes in gospel
            return "echo" if section != "bridge" else "lead"
            
    elif style == "jazz":
        # Different role assignments for jazz
        if tempo > 140 and "sax" in instrument_lower:
            return "lead"  # Fast jazz = sax leads
        elif "trumpet" in instrument_lower and section == "solo":
            return "lead"
            
    # Return the determined role
    return base_role
