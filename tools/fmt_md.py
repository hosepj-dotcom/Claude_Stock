#!/usr/bin/env python3
"""Pad Markdown tables so their pipes line up in a plain-text editor.

Usage: python3 tools/fmt_md.py FILE.md [FILE.md ...]   (rewrites files in place)

Columns whose body cells are all numbers are right-aligned; the rest are left-aligned.
"""
import re
import sys
import unicodedata

NUM = re.compile(r"^[−\-+≈~]?\s*(C\$|US\$|\$)?[−\-+]?[\d.,]+\s*(%|pp|k|M|B|T|x)?$")


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_sep(cells):
    return all(re.fullmatch(r":?-{1,}:?", c) for c in cells if c) and any(cells)


def fmt_table(lines):
    rows = [split_row(l) for l in lines]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    sep_idx = 1 if len(rows) > 1 and is_sep(rows[1]) else None
    body = [r for i, r in enumerate(rows) if i not in (0, sep_idx)]
    right = [
        bool(body) and all(NUM.match(r[c]) or r[c] in ("", "—") for r in body)
        and any(r[c] not in ("", "—") for r in body)
        for c in range(ncol)
    ]
    widths = [
        max(3, *(width(r[c]) for i, r in enumerate(rows) if i != sep_idx))
        for c in range(ncol)
    ]
    out = []
    for i, r in enumerate(rows):
        if i == sep_idx:
            cells = [("-" * (w - 1) + ":") if right[c] else "-" * w for c, w in enumerate(widths)]
        else:
            cells = []
            for c, w in enumerate(widths):
                pad = " " * (w - width(r[c]))
                cells.append(pad + r[c] if right[c] and i != 0 else r[c] + pad)
        out.append("| " + " | ".join(cells) + " |")
    return out


def fmt_text(text):
    lines, out, buf, in_code = text.split("\n"), [], [], False
    for line in lines + [""]:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and line.lstrip().startswith("|"):
            buf.append(line)
            continue
        if buf:
            out.extend(fmt_table(buf))
            buf = []
        out.append(line)
    return "\n".join(out[:-1])


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        new = fmt_text(src)
        if new != src:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"formatted {path}")
