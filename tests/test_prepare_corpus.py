import json
import tempfile
import unittest
from pathlib import Path

from lazy_normalizer import normalize_text
from prepare_corpus import build_corpus


class CorpusTests(unittest.TestCase):
    def test_alignment_collision_isolation_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "input.txt"
            source.write_text("Phone\nphone\nfone\nElephant!\nquick fox\n\n", encoding="utf-8")
            first, second = root / "a", root / "b"
            manifest = build_corpus(source, first)
            build_corpus(source, second)
            self.assertEqual(manifest["duplicates_removed"], 1)
            splits = []
            for split in ("train", "test"):
                rows = [json.loads(line) for line in (first / f"{split}_pairs.jsonl").read_text().splitlines()]
                self.assertTrue(rows)
                for row in rows:
                    self.assertEqual(row["lazy"], normalize_text(row["english"]))
                splits.append({row["lazy"] for row in rows})
            self.assertTrue(splits[0].isdisjoint(splits[1]))
            for file in first.iterdir():
                self.assertEqual(file.read_bytes(), (second / file.name).read_bytes())

    def test_rejects_unsplittable_corpus(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "input.txt"
            source.write_text("phone\nfone\n")
            with self.assertRaises(ValueError):
                build_corpus(source, root / "out")
