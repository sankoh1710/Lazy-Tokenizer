"""Phase 4.1: build reproducible aligned English/Lazy train and test data."""
import argparse
import hashlib
import json
import random
from pathlib import Path

from lazy_normalizer import normalize_text

ROOT = Path(__file__).resolve().parent


def build_corpus(source, output, test_fraction=0.2, seed=42):
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")
    raw = Path(source).read_bytes()
    groups = {}
    nonempty = 0
    for line in raw.decode("utf-8").splitlines():
        english = " ".join(line.split())
        if not english:
            continue
        nonempty += 1
        lazy = normalize_text(english)
        # Group normalized collisions so the same Lazy line cannot leak
        # across train and test (e.g. phone/fone or capitalization variants).
        groups.setdefault(lazy, {}).setdefault(english.casefold(), english)
    keys = sorted(groups)
    if len(keys) < 2:
        raise ValueError("Need at least two distinct normalized lines")
    random.Random(seed).shuffle(keys)
    test_count = max(1, min(len(keys) - 1, round(len(keys) * test_fraction)))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    counts = {}
    for split, selected in (("test", keys[:test_count]), ("train", keys[test_count:])):
        pairs = [{"english": english, "lazy": lazy}
                 for lazy in selected for english in groups[lazy].values()]
        counts[split] = {"pairs": len(pairs), "unique_lazy_lines": len(selected)}
        (output / f"{split}_pairs.jsonl").write_text(
            "".join(json.dumps(pair, ensure_ascii=False) + "\n" for pair in pairs), encoding="utf-8")
        # One line per normalized group avoids weighting collisions twice.
        (output / f"{split}_lazy.txt").write_text(
            "\n".join(selected) + "\n", encoding="utf-8")
    manifest = {
        "rules_version": "baseline-v0.1-wordwise",
        "normalizer_sha256": hashlib.sha256((ROOT / "lazy_normalizer.py").read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "seed": seed, "test_fraction": test_fraction,
        "nonempty_source_lines": nonempty,
        "duplicates_removed": nonempty - sum(c["pairs"] for c in counts.values()),
        "splits": counts,
        "note": "Rule-generated spellings, not human-verified phonetic transcriptions."
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "data/english_seed.txt")
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed")
    parser.add_argument("--test-fraction", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(build_corpus(args.source, args.output, args.test_fraction, args.seed), indent=2))
