"""Run: python -m unittest discover -s tests -v"""
import unittest
from lazy_normalizer import normalize_text, normalize_word


class WordTests(unittest.TestCase):
    def test_baseline_examples(self):
        cases = {
            "phone": "fone", "elephant": "elefant",
            "back": "bak", "what": "wat",
            "quick": "kwik", "box": "boks",
            "action": "akshon", "knee": "nee",
            "write": "rite", "through": "throo",
            "rough": "roo", "coughing": "kofing",
        }
        for word, expected in cases.items():
            with self.subTest(word=word):
                self.assertEqual(normalize_word(word), expected)

    def test_lowercase(self):
        self.assertEqual(normalize_word("PHONE"), "fone")


class TextTests(unittest.TestCase):
    def test_word_boundaries(self):
        self.assertEqual(normalize_text("knee write"), "nee rite")

    def test_spacing_punctuation(self):
        self.assertEqual(normalize_text("Phone,  what?\nWrite!"), "fone,  wat?\nrite!")

    def test_empty(self):
        self.assertEqual(normalize_text(""), "")

    def test_lowercase_policy(self):
        self.assertEqual(normalize_text("The PHONE!"), "the fone!")


if __name__ == "__main__":
    unittest.main()
