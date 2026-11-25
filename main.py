"""Two Robots in an Elevator — entry program.

Writes one line of awkward robot-to-robot elevator small talk to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Deterministic, stdlib only, no network, no randomness.
"""

import os

LINE = "You always stand exactly 0.4 metres away. Is that a protocol, or do I smell like hot circuitry?"


def validate(line):
    """The gate: 1-200 UTF-8 chars, not only whitespace, single line."""
    if not isinstance(line, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(line) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    return line


def write_entry(line, out_dir):
    """Write the line with no trailing newline, then read it back and
    re-validate the bytes on disk so a partial or mangled write is caught."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    if len(data) > 200:
        raise ValueError("entry must be at most 200 bytes, got %d" % len(data))
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read().decode("utf-8")
    if written != line:
        raise ValueError("round-trip check failed: file differs from entry")
    validate(written)
    return path


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(line, out_dir)


if __name__ == "__main__":
    main()
