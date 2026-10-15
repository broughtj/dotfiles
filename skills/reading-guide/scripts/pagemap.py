#!/usr/bin/env python3
"""
pagemap.py — extract a PDF's text layer keyed to its *printed* page numbers.

A reading guide is only useful if "p. 496" means what the reader sees on the
page. Scanned journal articles and book chapters almost never start at physical
page 1, so this infers the offset between physical and printed pages from the
running heads, then lets you extract and search by printed page number.

Usage
-----
  pagemap.py extract SOURCE.pdf [-o OUT.txt]
      Write the whole text layer with <<< p.NNN >>> markers before each page.
      Prints the inferred offset and any pages where the head disagreed.

  pagemap.py find SOURCE.pdf PATTERN [-i] [-C N]
      Regex-search the text layer; report each hit with its printed page number
      and N lines of context (default 2).

  pagemap.py map SOURCE.pdf
      Just print the physical -> printed page table.

Options
-------
  --offset N     Skip inference; printed = physical + N (physical is 1-based).
  --no-layout    Use plain pdftotext instead of -layout.

Requires `pdftotext` (poppler). If the PDF has no text layer, nothing here can
help — say so plainly rather than guessing at content.
"""

from __future__ import annotations

import argparse
import collections
import re
import shutil
import subprocess
import sys

PAGE_NUM = re.compile(r"(?<!\d)(\d{1,4})(?!\d)")


def extract_pages(pdf: str, layout: bool = True) -> list[str]:
    if shutil.which("pdftotext") is None:
        sys.exit("pdftotext not found. Install poppler (brew install poppler).")
    cmd = ["pdftotext"]
    if layout:
        cmd.append("-layout")
    cmd += [pdf, "-"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"pdftotext failed: {proc.stderr.strip()}")
    pages = proc.stdout.split("\f")
    # pdftotext emits a trailing empty chunk after the final form feed.
    if pages and not pages[-1].strip():
        pages.pop()
    if not pages or not any(p.strip() for p in pages):
        sys.exit(
            f"{pdf} has no extractable text layer. Read the PDF directly "
            "instead of trying to verify against it."
        )
    return pages


def candidates(page: str, edge: int = 3) -> list[int]:
    """Integers appearing in the top or bottom `edge` non-empty lines."""
    lines = [ln for ln in page.splitlines() if ln.strip()]
    if not lines:
        return []
    band = lines[:edge] + lines[-edge:]
    out: list[int] = []
    for ln in band:
        # Ignore lines that are mostly digits (tables of numbers).
        digits = sum(c.isdigit() for c in ln)
        if digits > max(4, len(ln.strip()) * 0.5):
            continue
        out.extend(int(m.group(1)) for m in PAGE_NUM.finditer(ln))
    return out


def infer_offset(pages: list[str]) -> tuple[int, collections.Counter]:
    """Modal (printed - physical) across pages whose head carries a number."""
    votes: collections.Counter = collections.Counter()
    for i, page in enumerate(pages, start=1):
        for n in candidates(page):
            off = n - i
            # A plausible offset: printed numbering does not run backwards far,
            # and front matter is rarely more than a few hundred pages.
            if -5 <= off <= 5000:
                votes[off] += 1
    if not votes:
        return 0, votes
    return votes.most_common(1)[0][0], votes


def printed_numbers(pages: list[str], offset: int) -> list[int]:
    return [i + offset for i in range(1, len(pages) + 1)]


def confirm(pages: list[str], offset: int) -> list[int]:
    """Physical pages (1-based) whose running head contradicts the offset."""
    bad = []
    for i, page in enumerate(pages, start=1):
        cands = candidates(page)
        if cands and (i + offset) not in cands:
            bad.append(i)
    return bad


def cmd_map(pages: list[str], offset: int) -> None:
    bad = confirm(pages, offset)
    print(f"physical pages: {len(pages)}    inferred offset: {offset:+d}")
    print(f"printed range:  {1 + offset}–{len(pages) + offset}")
    if bad:
        print(f"heads disagree on {len(bad)} page(s) (often plates/blank): {bad[:20]}")
    else:
        print("every page carrying a running-head number agrees with the offset")


def cmd_extract(pages: list[str], offset: int, out: str | None) -> None:
    chunks = [
        f"<<< p.{i + offset} >>>\n{page.rstrip()}\n"
        for i, page in enumerate(pages, start=1)
    ]
    text = "\n".join(chunks)
    if out:
        with open(out, "w") as fh:
            fh.write(text)
        print(f"wrote {out}  ({len(text):,} chars, printed pp. "
              f"{1 + offset}–{len(pages) + offset})")
    else:
        sys.stdout.write(text)


def cmd_find(pages: list[str], offset: int, pattern: str,
             ignore_case: bool, context: int) -> None:
    flags = re.IGNORECASE if ignore_case else 0
    rx = re.compile(pattern, flags)
    hits = 0
    for i, page in enumerate(pages, start=1):
        lines = page.splitlines()
        for j, line in enumerate(lines):
            if not rx.search(line):
                continue
            hits += 1
            lo, hi = max(0, j - context), min(len(lines), j + context + 1)
            print(f"--- p.{i + offset} (physical {i}, line {j + 1}) ---")
            for k in range(lo, hi):
                mark = ">" if k == j else " "
                print(f"{mark} {lines[k].rstrip()}")
            print()
    if not hits:
        print(f"no match for {pattern!r}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["extract", "find", "map"])
    ap.add_argument("pdf")
    ap.add_argument("pattern", nargs="?")
    ap.add_argument("-o", "--out")
    ap.add_argument("-i", "--ignore-case", action="store_true")
    ap.add_argument("-C", "--context", type=int, default=2)
    ap.add_argument("--offset", type=int)
    ap.add_argument("--no-layout", action="store_true")
    args = ap.parse_args()

    pages = extract_pages(args.pdf, layout=not args.no_layout)
    if args.offset is not None:
        offset = args.offset
    else:
        offset, votes = infer_offset(pages)
        if votes and votes.most_common(1)[0][1] < 3:
            print("warning: running heads are sparse; offset is a guess. "
                  "Pass --offset N if page numbers look wrong.", file=sys.stderr)

    if args.command == "map":
        cmd_map(pages, offset)
    elif args.command == "extract":
        cmd_extract(pages, offset, args.out)
    else:
        if not args.pattern:
            ap.error("find requires a PATTERN")
        cmd_find(pages, offset, args.pattern, args.ignore_case, args.context)


if __name__ == "__main__":
    main()
