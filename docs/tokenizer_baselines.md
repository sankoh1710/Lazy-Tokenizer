# Phase 4.2 — Pretrained tokenizer baselines

From the project folder, run:

```bash
git pull origin main
python -m pip install -r requirements-baselines.txt
python prepare_corpus.py
python compare_tokenizers.py
```

This downloads tokenizer files for `Qwen/Qwen2.5-0.5B-Instruct` and
`google-bert/bert-base-uncased`. No language-model weights, GPU, LoRA or training
are involved. The first run needs internet access; subsequent runs can reuse the
Hugging Face cache. Qwen is an explicit baseline choice, not a claim that it is
the exact checkpoint used in earlier experiments. Override it with `--models`.

The script reads held-out English/Lazy pairs. Each tokenizer receives both sides
as written, without prompts or added special tokens. It saves token pieces,
IDs, counts, unknown-token counts, decoded text and exact round-trip checks.
It also prints elephant/elefant and phone/fone as separate diagnostic probes;
these probes are not added to the held-out summary.

Reports live in `results/baselines/<model>/pairs.jsonl` and `summary.json`.
The tokenizer itself is saved beside them in `tokenizer/`. The summary records
library versions, input hash, vocabulary size and revision information. A single
checkpoint can be pinned with `--models OWNER/MODEL --revision COMMIT_SHA`.

Interpretation:

- IDs are local to each vocabulary. Equal IDs across models do not imply equal tokens.
- BERT uncased normalizes case and can change spacing during decoding. An exact
  round-trip failure is not automatically an implementation bug.
- Fewer tokens alone do not establish superiority. Vocabulary budgets, byte vs
  WordPiece representations, normalization, text length and unknowns differ.
- English/Lazy pairs can differ in capitalization as well as spelling. These
  reports describe the actual pipeline, not an isolated spelling-only effect.
- This small held-out corpus is exploratory. Do not tune our future tokenizer
  repeatedly against it; create validation data as the corpus grows.
- Tokenization results cannot prove why earlier model generation failed.

Run regression tests with `python -m unittest discover -s tests -v`. The comparison
unit tests use a small fake tokenizer to check report logic offline. A real run
with downloaded pretrained tokenizers remains necessary to obtain baselines.

Next, inspect the reported pieces together before Phase 4.3 tokenizer training.
