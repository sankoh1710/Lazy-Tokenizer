# Lazy Tokenizer

**Phase 4 of the Lazy Dictionary machine-learning experiments**

Lazy Tokenizer is an experimental project to design, train, inspect, and evaluate a tokenizer for the **Lazy Dictionary writing system**.

The goal is to investigate whether a tokenizer trained on Lazy-style text can represent its spelling patterns more naturally than an existing general-purpose tokenizer. This project follows earlier experiments fine-tuning Qwen with LoRA, where generating consistent Lazy Dictionary spellings proved difficult.

> **Research question:** How should a tokenizer represent text written under Lazy Dictionary's spelling rules, and what changes when we train that tokenizer on our own corpus?

## Background

Lazy Dictionary explores alternative, simplified spellings. For example, a rule such as `PH → F` can change `elephant` to `elefant`, and `phone` to `fone` (illustrative spellings; final rules are to be confirmed).

Our earlier experiments raised an important question: before teaching a model to produce these spellings, how does it **split and encode** the input and output text?

**Important distinction:** A tokenizer converts text into tokens and token IDs; it does **not** automatically learn or enforce spelling conversions. Spelling normalization, tokenization, and text generation are different stages of the pipeline. A custom tokenizer alone does not make a language model output correct Lazy spellings.

## Phase 4 roadmap

### 4A — Define and build

- [ ] **4.0 — Specify the Lazy rules.** Document substitutions, capitalization, exceptions, ordering, and expected outputs; create a small set of verified examples.
- [ ] **4.1 — Prepare a corpus.** Collect normal English and approved Lazy-transformed text, keep aligned pairs for evaluation, clean duplicates, and split data into training and held-out test sets.
- [ ] **4.2 — Establish baselines.** Inspect Qwen and BERT tokenizers on identical normal/Lazy inputs. Record token pieces, IDs, and counts.
- [ ] **4.3 — Train a tokenizer.** Start with a simple baseline (character- or word-level) and experiment with BPE using Hugging Face `tokenizers`. Choose vocabulary size and pre-tokenization deliberately.
- [ ] **4.4 — Inspect artifacts.** Explore vocabulary, merges (where applicable), token-to-ID mappings, special tokens, and encode/decode behavior.

### 4B — Evaluate

- [ ] **4.5 — Compare tokenization.** On held-out text, measure tokens per word/character, unknown-token rate, round-trip fidelity, and how consistently important Lazy patterns are segmented. Compare at similar vocabulary budgets where practical.
- [ ] **4.6 — Revisit earlier cases.** Study words such as `elephant → elefant` and `phone → fone`. Inspect what the tokenizer represents, without claiming tokenization alone solves conversion.

### 4C — Connect the concepts

- [ ] **4.7 — Study embeddings.** Trace text → tokens → token IDs → embedding lookup → vectors, connecting tokenizer behavior with linear algebra.
- [ ] **4.8 — Plan model integration.** Document vocabulary/embedding compatibility, whether embeddings need initialization or training, and how to test an adapted model without corrupting pretrained token meanings.

**Phase 5 (future):** Experiment with a language model using the tokenizer, with an explicitly designed embedding/model-training strategy.

## Conceptual pipeline

```text
English text
    |
    v
Lazy spelling rules / normalizer (if conversion is needed)
    |
    v
Lazy-style text
    |
    v
Tokenizer -> token pieces -> token IDs
                               |
                               v
                       Embedding lookup
                               |
                               v
                          Vectors
                               |
                               v
                    Language model (later)
```

The first experiments focus on the corpus, tokenizer, vocabulary, and evaluation—not model training.

## Planned tools

- Python
- Hugging Face `tokenizers`
- Hugging Face `transformers` (baseline comparisons)
- Jupyter / Google Colab (experiments)

Dependencies and reproducible setup instructions will be added when the first implementation is committed.

## Initial experiments

| Input | Purpose |
| --- | --- |
| `elephant` / `elefant` | Compare normal and Lazy spelling segmentation |
| `phone` / `fone` | Investigate a PH → F substitution |
| `photograph` / its approved Lazy form | Test related spelling patterns |
| Full Lazy-style sentences | Check performance beyond isolated words |

These examples are research prompts, not evidence that any tokenizer has already learned the intended mappings.

## Project status

**Planning — Phase 4.** No trained tokenizer, benchmark results, or model integration are claimed yet.

## Next step

Create a versioned **Lazy spelling specification** with verified examples and edge cases. Then build the first small corpus and baseline comparison notebook.

---

Part of the [Lazy Dictionary](https://lazydictionary.com/) experimentation journey.
