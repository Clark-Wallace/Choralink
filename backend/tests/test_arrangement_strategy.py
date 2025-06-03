"""
test_arrangement_strategy.py
============================
Tests for arrangement_strategy.py including:
- Difficulty scoring
- Skill-based simplification
- Role assignment

Author: Kaji (Bloom Architect)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from music21 import note
from backend.modules.arrangement_strategy import score_phrase, simplify_phrase, assign_role, assign_instrument_role

def mock_phrase(intervals):
    start_pitch = 60
    return [note.Note(start_pitch + i, quarterLength=0.25) for i in intervals]

def test_score():
    phrase = mock_phrase([0, 7, 0, 5, -3, 8])
    profile = {"range": (50, 80)}
    score = score_phrase(phrase, profile)
    print(f"Difficulty score: {score:.2f}")
    assert 0 <= score <= 10

def test_simplify():
    phrase = mock_phrase([0, 7, 0, 5, -3, 8])
    simplified = simplify_phrase(phrase, "beginner")
    for n in simplified:
        assert n.quarterLength >= 0.5
        assert not n.articulations

def test_role_assignments():
    print("\n=== Basic Role Assignment Tests ===")
    print("Verse, measure 0:", assign_role(0, "verse", "gospel"))
    print("Verse, measure 1:", assign_role(1, "verse", "gospel"))
    print("Chorus, measure 2:", assign_role(2, "chorus", "gospel"))

def test_instrument_role_scenarios():
    print("\n=== Instrument Role Assignment Scenarios ===")
    
    # Scenario 1: Lead instrument in verse
    context1 = {
        "style": "gospel",
        "section": "verse",
        "tempo": 100,
        "density": 0.3,
        "measure_index": 0
    }
    print("\nScenario 1 - Saxophone in sparse verse:")
    print(f"  Context: {context1}")
    print(f"  Role: {assign_instrument_role('saxophone', context1)}")
    
    # Scenario 2: Echo instrument
    context2 = {
        "style": "gospel",
        "section": "verse",
        "tempo": 120,
        "density": 0.5,
        "measure_index": 1
    }
    print("\nScenario 2 - Flute in gospel verse:")
    print(f"  Context: {context2}")
    print(f"  Role: {assign_instrument_role('flute', context2)}")
    
    # Scenario 3: Interjector at phrase boundary
    context3 = {
        "style": "gospel",
        "section": "verse",
        "tempo": 110,
        "density": 0.6,
        "measure_index": 3
    }
    print("\nScenario 3 - Trumpet at phrase boundary:")
    print(f"  Context: {context3}")
    print(f"  Role: {assign_instrument_role('trumpet', context3)}")
    
    # Scenario 4: Harmony in dense section
    context4 = {
        "style": "gospel",
        "section": "chorus",
        "tempo": 120,
        "density": 0.8,
        "measure_index": 0
    }
    print("\nScenario 4 - Saxophone in dense chorus:")
    print(f"  Context: {context4}")
    print(f"  Role: {assign_instrument_role('saxophone', context4)}")
    
    # Scenario 5: Fallback for unknown instrument
    context5 = {
        "style": "classical",
        "section": "verse",
        "tempo": 80,
        "density": 0.4,
        "measure_index": 0
    }
    print("\nScenario 5 - Unknown instrument fallback:")
    print(f"  Context: {context5}")
    print(f"  Role: {assign_instrument_role('kazoo', context5)}")

def test_difficulty_thresholds():
    print("\n=== Difficulty Threshold Tests ===")
    
    # Test phrases with different complexities
    simple_phrase = mock_phrase([0, 2, 2, 0])  # Simple stepwise
    medium_phrase = mock_phrase([0, 4, 7, 12, 7, 4, 0])  # Some leaps
    complex_phrase = mock_phrase([0, 12, -5, 8, -3, 15, 0])  # Large leaps
    
    profile = {"range": (40, 80)}
    
    print(f"\nSimple phrase score: {score_phrase(simple_phrase, profile):.2f}")
    print(f"Medium phrase score: {score_phrase(medium_phrase, profile):.2f}")
    print(f"Complex phrase score: {score_phrase(complex_phrase, profile):.2f}")
    
    # Test simplification for different levels
    print("\n=== Simplification Tests ===")
    for level in ["beginner", "intermediate", "advanced"]:
        simplified = simplify_phrase(complex_phrase, level)
        print(f"\n{level.capitalize()} simplification:")
        print(f"  Original durations: {[n.quarterLength for n in complex_phrase[:3]]}")
        print(f"  Simplified durations: {[n.quarterLength for n in simplified[:3]]}")

if __name__ == "__main__":
    print("=== ARRANGEMENT STRATEGY TEST SUITE ===\n")
    test_score()
    test_simplify()
    test_role_assignments()
    test_instrument_role_scenarios()
    test_difficulty_thresholds()
    print("\n=== ALL TESTS COMPLETE ===")
    
    # Integration test suggestion
    print("\n💡 To test full integration, run:")
    print("python3 backend/run_choralink.py --input [file] --instrument saxophone --difficulty beginner")
