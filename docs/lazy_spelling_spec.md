# Phase 4.0 — Lazy spelling specification (baseline)

**Version:** `baseline-v0.1-wordwise`

**Status:** Baseline extracted from the existing Lazy Dictionary implementation. Not yet a finalized linguistic specification.

**Source of truth:** [Lazy Dictionary — lazySpell.ts](https://github.com/sankoh1710/Lazy-Dictionary/blob/main/artifacts/lazy-dictionary/src/lib/lazySpell.ts)

## Purpose

Before training a tokenizer, establish precisely which text it will be trained on. The existing `toLazy(word)` function is a deterministic **spelling normalizer**. A tokenizer is different: it splits text into tokens and maps them to IDs. Training a tokenizer on normalized text does not itself teach a model to rewrite English.

## Current ordered rules

The existing implementation first lowercases input, then applies these replacements **in this exact sequence**.

| Order | Pattern | Replacement | Scope / note |
| --- | --- | --- | --- |
| 0 | uppercase | lowercase | Entire input |
| 1 | `^kn` | `n` | Beginning of input |
| 2 | `^wr` | `r` | Beginning of input |
| 3 | `wh` | `w` | All occurrences |
| 4 | `tion` | `shon` | All occurrences |
| 5 | `ough$` | `oo` | End of input |
| 6 | `ough` | `of` | Remaining occurrences |
| 7 | `ph` | `f` | All occurrences |
| 8 | `ck` | `k` | All occurrences |
| 9 | `qu` | `kw` | All occurrences |
| 10 | `q` | `k` | All occurrences |
| 11 | `x` | `ks` | All occurrences |
| 12 | `gh` | *(remove)* | All occurrences |
| 13 | `c([eiy])` | `s$1` | Soft c before e/i/y |
| 14 | `c(?!h)` | `k` | Remaining c unless followed by h |
| 15 | `([bdfgklmnprstz])\\1` | `$1` | Double listed consonants collapse to one |

These are implementation rules, not necessarily linguistically correct in every case.

## Initial illustrative pairs

Derived from the current rules; these are a starter test set, not corpus data:

| English | Baseline Lazy |
| --- | --- |
| phone | fone |
| elephant | elefant |
| back | bak |
| what | wat |
| quick | kwik |
| box | boks |
| action | akshon |
| knee | nee |
| write | rite |

## Questions to test before freezing a standard

1. **Word vs. sentence boundaries:** `^kn` and `^wr` match only the beginning of the entire input, not every word in a sentence. Decide whether to convert word by word.
2. **Ambiguous pronunciation:** `ough` has many pronunciations; the current two rules are approximate and can produce unnatural spellings.
3. **Transformation order:** Rules interact. A future revision must preserve an explicit order and regression tests.
4. **Capitalization and punctuation:** The function lowercases everything; decide if case and nonletters should be preserved.
5. **Exceptions and semantics:** The normalizer has no dictionary-based or context-aware exceptions.
6. **Tokenization objective:** Compare BPE or other tokenizers on the same held-out Lazy corpus, with vocabulary size and normalization kept explicit.

## Acceptance criteria for 4.0

- [x] Record the current rules and their order.
- [x] Record initial expected examples.
- [x] Use these rules as a provisional baseline, not a final alphabet.
- [x] Apply rules word by word using `normalize_text`; preserve separators and lowercase English words.
- [x] Add automated regression tests for baseline conversions.
- [x] Version the specification before corpus generation.

## Next stage

**4.1 — Corpus preparation:** Generate examples from *approved* rules, then make train/test splits for tokenizer training and evaluation.
