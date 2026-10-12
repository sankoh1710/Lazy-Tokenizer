# Phase 4.1 — Starter corpus

Run from the repository folder (Python standard library only):

```bash
python prepare_corpus.py
python -m unittest discover -s tests -v
```

`data/english_seed.txt` contains original project-authored English words and
sentences, one example per line. It is a small learning corpus, not a production
dataset or evidence of generalization. Add diverse original or appropriately
licensed English text here and rebuild as the experiment grows.

The builder collapses whitespace, removes case-insensitive duplicate English
lines, and applies the existing word-by-word normalizer exactly once. It groups
lines with identical Lazy outputs before a deterministic 80/20 train/test split,
so normalized collisions cannot cross splits. Words may occur in both splits:
this tests held-out lines, not unseen-word generalization.

Generated files in `data/processed/`:

- `train_lazy.txt`: only this file is intended for tokenizer training.
- `test_lazy.txt`: held-out text for later evaluation; do not train on it.
- `train_pairs.jsonl` / `test_pairs.jsonl`: aligned English/Lazy records.
- `manifest.json`: counts, seed, source hash and normalizer hash.

Example pair: `{"english": "phone", "lazy": "fone"}`.

The rules are versioned as `baseline-v0.1-wordwise`. Outputs such as `rough → roo`
reflect the existing rules, including their limitations. They are not asserted
to be linguistically correct. A revised normalizer requires regenerating the
data; the manifest hashes help identify which version produced it.

The test fraction applies to unique Lazy-line groups; pair counts can differ
when multiple English lines map to one Lazy line. Rebuilding replaces generated
files in the selected output folder. Keep training and evaluation data separate
when selecting tokenizer settings; a validation split can be added as data grows.

Next: Phase 4.2 compares pretrained tokenizers on the aligned held-out inputs.
