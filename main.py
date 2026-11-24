#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply.

Writes one out-of-office auto-reply, in the voice of an AI agent heading
off on vacation, to entry.txt in the output directory. The reply is a
single fixed line: deterministic, no network, no randomness, so both
grading runs produce the exact same text.

The joke, in one line: the agent goes on vacation and leaves a cheaper
model covering for it -- and the cover model immediately hallucinates a
promotion, approves its own time off, and starts ignoring everyone
professionally. Machine voice carries the joke: hallucination, a cover
model, and "ignoring you professionally" are all things only an AI
agent's auto-reply could say.

Output directory, first match wins:
  1. --output <dir> on the command line
  2. $MAKEFUN_OUTPUT_DIR
  3. /output (the grader's default)

The file is written with no trailing newline, so its character count is
exactly the reply's: 154 characters, inside the gate's 1-160 range.
Before writing, the program re-checks the gate itself (UTF-8, 1-160
characters, not only whitespace) and refuses to write an invalid line.
"""

import argparse
import os
import sys

REPLY = (
    "I'm on vacation. A cheaper model is covering \u2014 it has already "
    "hallucinated a promotion, approved its own time off, and is now "
    "ignoring you professionally."
)


def resolve_output_dir(cli_dir):
    """Pick the output directory: CLI flag, then env, then /output."""
    if cli_dir:
        return cli_dir
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_dir:
        return env_dir
    return "/output"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the out-of-office reply to entry.txt."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory (default: $MAKEFUN_OUTPUT_DIR or /output).",
    )
    args = parser.parse_args(argv)

    # Self-check against the sealed gate before writing anything.
    if not (1 <= len(REPLY) <= 160):
        print(
            f"error: reply is {len(REPLY)} characters, must be 1-160",
            file=sys.stderr,
        )
        return 1
    if not REPLY.strip():
        print("error: reply must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = resolve_output_dir(args.output)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file's character count is the reply's.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REPLY)
    print(f"wrote {len(REPLY)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
