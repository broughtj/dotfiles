#!/usr/bin/env python3
"""Scaffold a slide deck in the course theme.

    python3 ~/.claude/skills/slides/scripts/new-deck.py --out slides --stem ch03-hedging \
        --title "Hedging with Futures" --subtitle "Hull, Chapter 3" --course "DATA 5695 / 6695" \
        [--institute "..."] [--author "..."] [--date "October 2026"] [--source "Hull ch. 3 PDF"] \
        [--justfile-root .] [--no-check] [--force]

Writes <out>/<stem>.qmd (header + skeleton body), installs the usu-slides Quarto extension
into <out>/_extensions if missing (from GitHub, or from --ext-path / $USU_SLIDES_EXT),
writes <out>/check-<stem>.jl unless --no-check, and creates or extends a justfile:
  * no justfile at --justfile-root  -> copy justfile.template (parameterized `just deck <stem>`)
  * justfile with a `decks := "..."` line -> append the stem to that list
  * any other justfile               -> append a namespaced <stem>* recipe block
Existing files are never overwritten unless --force (the justfile is only ever appended to).
"""
import argparse, datetime, os, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = HERE / "assets"

def fill(text, sub):
    for k, v in sub.items():
        text = text.replace("{{" + k + "}}", v)
    return text

SKELETON = '''

# Part I: {{PART1}} {background-color="#1B2A4A"}


## Road Map

| Part | Topic | Source |
|------|-------|--------|
| **I** | ... | |
| **II** | ... | |

::: {.fragment}
::: {.callout-tip appearance="minimal" icon="false"}
One sentence on why this chapter matters for the rest of the course.
:::
:::


## First Content Slide

- Three to six bullets, one line each
- Or two `.columns` at 50% / 50%

::: {.fragment}
::: {.callout-note appearance="minimal" icon="false"}
The takeaway for this slide, in one or two sentences.
:::
:::


# Part II: Wrap-Up {background-color="#1B2A4A"}


## What to Take Away

::: {.columns}
::: {.column width="50%"}
**Concepts**

- ...
:::
::: {.column width="50%"}
**Machinery**

- ...
:::
:::

::: {.fragment}
**Questions?**
:::
'''

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="folder for the deck, e.g. slides")
    ap.add_argument("--stem", required=True, help="file stem, e.g. ch03-hedging")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--course", required=True, help='e.g. "DATA 5695 / 6695"')
    ap.add_argument("--institute", default="Data Analytics & Information Systems, Utah State University")
    ap.add_argument("--author", default="Tyler J. Brough")
    ap.add_argument("--date", default=datetime.date.today().strftime("%B %Y"))
    ap.add_argument("--source", default="(describe the source material here)")
    ap.add_argument("--part1", default="Introduction")
    ap.add_argument("--justfile-root", default=None, help="where the justfile lives (default: git root, else --out's parent)")
    ap.add_argument("--no-check", action="store_true", help="skip the check-<stem>.jl skeleton")
    ap.add_argument("--ext-path", default=os.environ.get("USU_SLIDES_EXT"),
                    help="local checkout of quarto-usu-slides to install from instead of GitHub")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", a.stem):
        sys.exit(f"stem must be a plain identifier (letters, digits, - _), got {a.stem!r}")
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)

    # justfile root: explicit, else git toplevel, else parent of out
    if a.justfile_root:
        root = pathlib.Path(a.justfile_root)
    else:
        root = out.resolve()
        while root != root.parent and not (root / ".git").exists():
            root = root.parent
        if not (root / ".git").exists():
            root = out.resolve().parent
    try:
        rel_dir = str(out.resolve().relative_to(root.resolve()))
    except ValueError:
        sys.exit(f"--out {out} is not inside justfile root {root}")

    sub = dict(STEM=a.stem, TITLE=a.title, SUBTITLE=a.subtitle, COURSE=a.course, INSTITUTE=a.institute,
               AUTHOR=a.author, DATE=a.date, SOURCE_NOTE=a.source, DIR=rel_dir, PART1=a.part1)
    made = []

    qmd = out / f"{a.stem}.qmd"
    if qmd.exists() and not a.force:
        sys.exit(f"refusing to overwrite {qmd} (use --force)")
    qmd.write_text(fill((ASSETS / "header.yml").read_text(), sub) + fill(SKELETON, sub))
    made.append(qmd)

    # GitHub installs are namespaced by owner (_extensions/broughtj/usu-slides); a local-path
    # install is not (_extensions/usu-slides). Accept either.
    def ext_dir():
        for p in (out / "_extensions" / "broughtj" / "usu-slides", out / "_extensions" / "usu-slides"):
            if (p / "_extension.yml").exists():
                return p
    if ext_dir() is None:
        src = a.ext_path or "broughtj/quarto-usu-slides"
        r = subprocess.run(["quarto", "add", src, "--no-prompt"], cwd=out, capture_output=True, text=True)
        if r.returncode != 0 or ext_dir() is None:
            sys.exit(f"could not install the usu-slides extension from {src}:\n{r.stderr or r.stdout}")
        made.append(ext_dir())

    if not a.no_check:
        chk = out / f"check-{a.stem}.jl"
        if not chk.exists() or a.force:
            chk.write_text(fill((ASSETS / "check-template.jl").read_text(), sub)); made.append(chk)

    jf = root / "justfile"
    if not jf.exists():
        jf.write_text(fill((ASSETS / "justfile.template").read_text(), sub)); made.append(jf)
        how = "created"
    else:
        text = jf.read_text()
        m = re.search(r'^decks\s*:=\s*"([^"]*)"', text, re.M)
        if m:
            decks = m.group(1).split()
            if a.stem not in decks:
                decks.append(a.stem)
                text = text[:m.start(1)] + " ".join(decks) + text[m.end(1):]
                jf.write_text(text)
            how = "added to `decks`"
        elif re.search(rf"^{re.escape(a.stem)}:", text, re.M):
            how = "already has recipes for this stem"
        else:
            jf.write_text(text.rstrip("\n") + "\n" + fill((ASSETS / "justfile-block.template").read_text(), sub))
            how = "appended a namespaced recipe block"
        made.append(jf)

    print("scaffolded", a.stem)
    for p in made: print("  ", p)
    print("justfile:", jf, "-", how)
    print("next: write the slide body in", qmd, "then render with",
          f"`just deck {a.stem}`" if "decks :=" in jf.read_text() else f"`just {a.stem}`")

if __name__ == "__main__":
    main()
