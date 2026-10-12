"""Phase 4.0: word-by-word Lazy spelling normalizer (not a tokenizer).

Mirrors the ordered rules in Lazy Dictionary's TypeScript toLazy function.
"""
import re

# Only English A-Z word spans; punctuation and whitespace are preserved.
_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
_DOUBLE_CONSONANT = re.compile(r"([bdfgklmnprstz])\1")


def normalize_word(word: str) -> str:
    """Apply the original ordered rules to a single word."""
    w = word.lower()
    w = re.sub(r"^kn", "n", w)
    w = re.sub(r"^wr", "r", w)
    w = w.replace("wh", "w")
    w = w.replace("tion", "shon")
    w = re.sub(r"ough$", "oo", w)
    w = w.replace("ough", "of")
    w = w.replace("ph", "f")
    w = w.replace("ck", "k")
    w = w.replace("qu", "kw")
    w = w.replace("q", "k")
    w = w.replace("x", "ks")
    w = w.replace("gh", "")
    w = re.sub(r"c([eiy])", r"s\1", w)
    w = re.sub(r"c(?!h)", "k", w)
    w = _DOUBLE_CONSONANT.sub(r"\1", w)
    return w


def normalize_text(text: str) -> str:
    """Normalize English-letter words independently, preserving separators.

    Converted words are lowercased, like in the original toLazy().
    Unicode non-ASCII letters are not changed; this is a known limitation.
    """
    return _WORD.sub(lambda m: normalize_word(m.group()), text)


if __name__ == "__main__":
    print(normalize_text("The phone, quick fox and knight write!"))
