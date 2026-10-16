"""Phase 4.2: inspect pretrained tokenizers; no model weights or training."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_MODELS = ["Qwen/Qwen2.5-0.5B-Instruct", "google-bert/bert-base-uncased"]


def inspect_text(tokenizer, text):
    ids = tokenizer.encode(text, add_special_tokens=False)
    decoded = tokenizer.decode(ids, skip_special_tokens=False,
                               clean_up_tokenization_spaces=False)
    return {"text": text, "tokens": tokenizer.convert_ids_to_tokens(ids),
            "ids": ids, "token_count": len(ids),
            "unknown_count": sum(i == tokenizer.unk_token_id for i in ids),
            "decoded": decoded, "exact_round_trip": decoded == text}


def load_pairs(path):
    pairs = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        pair = json.loads(line)
        if not isinstance(pair, dict) or any(
            not isinstance(pair.get(key), str) or not pair[key].strip()
            for key in ("english", "lazy")
        ):
            raise ValueError(f"Invalid English/Lazy pair on line {number}")
        pairs.append(pair)
    if not pairs:
        raise ValueError("Input contains no pairs; run prepare_corpus.py first")
    return pairs


def compare(pairs, tokenizer):
    return [{side: inspect_text(tokenizer, pair[side])
             for side in ("english", "lazy")} for pair in pairs]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/processed/test_pairs.jsonl")
    parser.add_argument("--output", type=Path, default=ROOT / "results/baselines")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--revision", default="main", help="Use a commit SHA to pin a single model")
    args = parser.parse_args()
    pairs = load_pairs(args.input)
    try:
        from transformers import AutoTokenizer
    except ImportError as error:
        raise SystemExit("Install dependencies: python -m pip install -r requirements-baselines.txt") from error
    args.output.mkdir(parents=True, exist_ok=True)
    for model in args.models:
        print(f"\nLoading tokenizer only: {model}", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(model, revision=args.revision,
                                                use_fast=True, trust_remote_code=False)
        rows = compare(pairs, tokenizer)
        # Save the actual tokenizer used, even if upstream 'main' later changes.
        folder = args.output / model.replace("/", "--")
        folder.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(folder / "tokenizer")
        (folder / "pairs.jsonl").write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        summary = {
            "model": model, "requested_revision": args.revision,
            "resolved_commit": tokenizer.init_kwargs.get("_commit_hash"),
            "transformers_version": importlib.metadata.version("transformers"),
            "tokenizers_version": importlib.metadata.version("tokenizers"),
            "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
            "tokenizer_class": type(tokenizer).__name__, "vocabulary_size": len(tokenizer),
            "pair_count": len(rows), "add_special_tokens": False,
            "sides": {}
        }
        for side in ("english", "lazy"):
            total = sum(row[side]["token_count"] for row in rows)
            summary["sides"][side] = {
                "total_tokens": total, "tokens_per_example": total / len(rows),
                "unknown_tokens": sum(row[side]["unknown_count"] for row in rows),
                "exact_round_trips": sum(row[side]["exact_round_trip"] for row in rows)
            }
        (folder / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary["sides"], indent=2))
        for pair in ({"english": "elephant", "lazy": "elefant"},
                     {"english": "phone", "lazy": "fone"}):
            for side, result in compare([pair], tokenizer)[0].items():
                print(f"{side}: {result['text']!r} -> {result['tokens']} -> {result['ids']}")
        print(f"Saved reports and tokenizer to {folder}")


if __name__ == "__main__":
    main()
