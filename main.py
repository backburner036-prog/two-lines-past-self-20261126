"""Entry for make.fun bounty "Two Lines to Your Past Self".

Two lines, one warning sent back to a past self. The entry is built on
the recipe the judge brief weighs — concrete moment, clear cause and
effect, tightness, freshness, a voice written to one person:

  1. Concrete moment: line one names a single moment exactly — a
     Friday, 4:47 PM, one pull request titled 'quick fix'. A time, a
     decision, and a named artefact, not a vague phase of life.
  2. Cause-and-effect trace: line two follows the chain — that one
     line took checkout down for nine hours, and the consequence
     stuck: ever since, every deploy waits for Monday and two
     reviewers. The moment mattered because the rule it created is
     still in force.
  3. Tightness: no wasted words; each line is one sentence, and the
     two lines work as one — the warning sets up the moment, the
     reason lands the consequence.
  4. Freshness: a deploy-Friday story every engineer recognises,
     told with a specific time and a specific title instead of the
     generic "don't deploy on Friday" lesson the field is full of.
  5. Clean read: no control characters, no trailing whitespace, one
     sentence per line — the judge reads it out loud exactly as
     written.

Head-to-head against the other two candidates in the analysis:
K2 (deleted folder named final_FINAL_v2) names its artefact but its
consequence — a week rebuilding a logo from a screenshot — leaves no
lasting rule behind. K3 ("we'll fix the tests later", March sprint
review) has a concrete cost (fourteen months) but a vague moment: no
day, no time, no named artefact. K1 wins on both judge weights: the
most concrete moment and the clearest cause-and-effect chain.

One redaction fix from the analysis draft: "4:47 p.m." became
"4:47 PM" so the abbreviation's periods cannot be misread as extra
sentence breaks. Meaning unchanged.
"""

from pathlib import Path

LINE1 = "Don't merge the Friday 4:47 PM pull request titled 'quick fix'."
LINE2 = "That one line took down checkout for nine hours, and ever since, every deploy waits for Monday and two reviewers."

TEXT = LINE1 + "\n" + LINE2

OUT = Path("/output/entry.txt")


def check_len(text, lo=1, hi=280):
    size = len(text)
    assert lo <= size <= hi, f"entry must be {lo}-{hi} chars, got {size}"
    assert text.strip(), "entry must not be whitespace only"
    return size


def check_gate(text):
    """Mirror the bounty gate, plus the judge's two-line shape.

    Sealed gate: /output/entry.txt is UTF-8 text of 1-280 characters,
    not whitespace only. On top of that the entry must be exactly two
    lines, one sentence per line (a single sentence terminator each),
    with no control characters and no leading/trailing whitespace on
    any line — the judge reads the warning out loud, so anything that
    cannot be read cleanly fails here, not on stage.
    """
    text.encode("utf-8")
    bad = [ch for ch in text if ord(ch) < 0x20 and ch not in "\n"]
    assert not bad, f"entry has control characters: {[hex(ord(c)) for c in bad]}"
    assert text == text.strip(), "entry must not start/end with whitespace"
    lines = text.split("\n")
    assert len(lines) == 2, f"entry must be exactly 2 lines, got {len(lines)}"
    for i, line in enumerate(lines, start=1):
        assert line == line.strip(), f"line {i} must not start/end with whitespace"
        assert line, f"line {i} must not be empty"
        terminators = sum(line.count(c) for c in ".!?")
        assert terminators == 1, f"line {i} must be one sentence, got {terminators} terminators"
    return check_len(text)


def save_entry(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write(text)


def main():
    check_gate(TEXT)
    save_entry(OUT, TEXT)
    saved = OUT.read_text(encoding="utf-8")
    assert saved == TEXT, "round-trip mismatch"
    print(f"wrote {len(TEXT)} chars to {OUT}")
    for i, line in enumerate(TEXT.split("\n"), start=1):
        print(f"line {i}: {len(line)} chars")


if __name__ == "__main__":
    main()
