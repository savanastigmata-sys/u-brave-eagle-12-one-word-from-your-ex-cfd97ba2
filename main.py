"""One Word From Your Ex — make.fun entry (program/v1).

Writes exactly one word to $MAKEFUN_OUTPUT_DIR/entry.txt: the word the
entrant's ex would use to describe them. Nothing else.

The word: "loading" — always loading, never finished, never delivered.
An ex would say it; it lands instantly, it stings because it is true.
"""

import os
import sys

WORD = "loading"

MAX_CHARS = 24
MIN_CHARS = 1


def resolve_output_dir():
    """Return the output directory for the entry artifact.

    The grader sets MAKEFUN_OUTPUT_DIR; fall back to ./output so the
    program also runs locally for a quick check.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(word):
    """Enforce the sealed gate: UTF-8 text, 1-24 chars, not only
    whitespace, exactly one word on exactly one line. The judge's
    first criterion is a real word an ex would say about a partner,
    so the entry must be letters only — no digits, punctuation,
    hyphens or control characters that would read as a phrase."""
    if not isinstance(word, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(word) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(word))
        )
    if not word.strip():
        raise ValueError("entry must not be only whitespace")
    if len(word.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not word.isalpha():
        raise ValueError("entry must be letters only, got %r" % word)
    word.encode("utf-8")
    return word


def main():
    word = validate(WORD)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    # Read back and re-validate: the artifact on disk must be exactly
    # the word that was validated, byte for byte.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != word:
        raise ValueError("read-back mismatch: %r != %r" % (written, word))
    validate(written)
    print("wrote %s (%d bytes)" % (path, len(word.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
