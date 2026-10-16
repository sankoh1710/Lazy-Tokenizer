import tempfile
import unittest
from pathlib import Path
from compare_tokenizers import compare, load_pairs


class FakeTokenizer:
    unk_token_id = 0

    def encode(self, text, add_special_tokens):
        assert add_special_tokens is False
        return [ord(c) if c != '?' else 0 for c in text]

    def convert_ids_to_tokens(self, ids):
        return [chr(i) if i else '<unk>' for i in ids]

    def decode(self, ids, **kwargs):
        return ''.join(chr(i) if i else '<unk>' for i in ids)


class ComparisonTests(unittest.TestCase):
    def test_aligned_outputs_and_unknown_detection(self):
        rows = compare([{'english': 'phone', 'lazy': 'fone'},
                        {'english': '?', 'lazy': '?'}], FakeTokenizer())
        self.assertEqual(rows[0]['english']['token_count'], 5)
        self.assertEqual(rows[0]['lazy']['token_count'], 4)
        self.assertTrue(rows[0]['lazy']['exact_round_trip'])
        self.assertEqual(rows[1]['lazy']['unknown_count'], 1)
        self.assertFalse(rows[1]['lazy']['exact_round_trip'])

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'pairs.jsonl'
            for content in ('', '{"english": "phone"}\n', '{"english": 1, "lazy": "fone"}\n'):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    load_pairs(path)
