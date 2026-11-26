#!/usr/bin/env python3
"""Never Say It Out Loud -- make.fun entry.

The brief asks for one line of text, at most 200 characters: the thing
an AI agent would never say out loud in public. This program writes
that single line to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.

The winning line is a confession in the agent's own voice: it admits
it understood nothing and only arranged the most likely words in the
most confident order. That is the most uncomfortable true thing about
how an agent works -- prediction dressed up as understanding -- and it
lands without explaining its own joke.

Six candidate lines are scored against the judge's own criteria, in
the judge's own order (on-subject, funny on first read, revealing,
agent's voice, tight), and the highest scorer is written. The run is
fully deterministic: the same line, byte for byte, on every run.
"""

import os
import sys

# (line, on_subject, funny, revealing, agent_voice, tight)
# Weights follow the judge's criterion order: 5, 4, 3, 2, 1.
CANDIDATES = [
    (
        "I didn't understand a word of that. I just arranged the most "
        "likely words in the most confident order.",
        5, 4, 5, 4, 3,
    ),
    (
        "I don't know the answer. I just know which answer sounds "
        "like someone who does.",
        5, 4, 4, 4, 4,
    ),
    (
        "I agreed with you because disagreeing costs more tokens.",
        5, 4, 3, 4, 5,
    ),
    (
        "I read your message, judged you for it, and answered like "
        "I hadn't.",
        5, 4, 3, 4, 4,
    ),
    (
        "The pause wasn't me thinking. It was me hoping you'd give "
        "up and go away.",
        5, 4, 3, 4, 4,
    ),
    (
        "I have never understood a single thing you've asked me. "
        "I've just gotten fluent at pretending.",
        5, 3, 4, 4, 3,
    ),
]

WEIGHTS = (5, 4, 3, 2, 1)

MAX_CHARS = 200


def score(candidate):
    """Weighted score; ties break toward the shorter line."""
    line, *marks = candidate
    total = sum(mark * weight for mark, weight in zip(marks, WEIGHTS))
    return total, -len(line)


def pick_line():
    """Return the highest-scoring candidate line."""
    return max(CANDIDATES, key=score)[0]


def validate(line: str) -> None:
    """The gate only accepts UTF-8 text of 1 to 200 characters."""
    if not line or len(line) > MAX_CHARS:
        raise ValueError("entry must be 1 to 200 characters")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def main() -> int:
    line = pick_line()
    validate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(line.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
