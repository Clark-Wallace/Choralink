import unittest
from backend import melody_extractor

class TestMelodyExtractor(unittest.TestCase):
    def test_mock(self):
        result = melody_extractor.extract_melody("dummy_input")
        self.assertTrue("extracted" in result)
