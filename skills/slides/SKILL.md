---
name: slides
description: Build a lecture slide deck in Tyler's course theme (Metropolis Beamer PDF in the navy/gold palette with Fira fonts, plus a matching revealjs HTML deck and Typst handout) from any input - a textbook chapter PDF, an old Jupyter notebook, Quarto or Markdown notes, code, or a topic description, optionally guided by a pre-existing document (an older deck or notes) that informs emphasis and ordering without dictating format. Installs the usu-slides Quarto extension (github.com/broughtj/quarto-usu-slides) beside the deck, scaffolds the .qmd, creates or extends the justfile, writes a Julia check script for every number quoted on the slides, renders all three formats, and reviews the Beamer output visually. Use for "/slides <input>", "make slides for", "build a deck from", "turn these notes into slides", or "same slides as ch02 but for".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, Skill
---

# Slides

Base directory: `~/.claude/skills/slides`

## Purpose

Turn source material into a lecture deck that looks and builds exactly like the existing
course decks: one `slides/<stem>.qmd`, three outputs (`<stem>.html`, `<stem>-beamer.pdf`,
`<stem>-handout.pdf`) produced by the `usu-slides` Quarto extension installed in
`slides/_extensions/broughtj/usu-slides/`, a `justfile` recipe set, and
`check-<stem>.jl` that reproduces every number printed on the slides. The Beamer PDF is
the primary deliverable.

## When to activate

- `/slides <input> [options]`
- "make slides for chapter 3", "build a deck from this notebook", "turn these notes into
  slides", "same as the ch02 deck but for ..."

## Arguments

| Form | Meaning |
|---|---|
| `<input>` | A file (`.pdf`, `.ipynb`, `.qmd`, `.md`, `.py`, `.jl`, `.tex`), a folder of such files, or a quoted topic description. Several inputs may be given. |
| `--out DIR` | Deck folder. Default: `slides/` at the repository root if it exists, else beside the input. |
| `--stem NAME` | File stem, e.g. `ch03-hedging`. Default: derived from chapter number and title. |
| `--course "DATA 5695 / 6695"` | Overrides the course inferred from the repo or folder name. |
| `--ref FILE` | A pre-existing document to consult while writing: earlier slides on the same material (`.tex`, `.Rmd`, `.pdf`, `.pptx`), lecture notes, a notebook, or a prior deck from another course. Several may be given. It guides emphasis and ordering; it does not set the format. See step 2b. |
| `--scope full\|core` | `full` covers the whole source; `core` only the parts the input itself emphasizes. Default: ask if the source is a full textbook chapter, otherwise `core`. |
| `--beamer-only` | Render only the PDF (the `.qmd` still carries all three formats). |
| `--no-julia` | No code on the slides and no check script. |

## Workflow

### 1. Read the input completely

Read every input file in full before planning (PDFs page by page with the `pages`
parameter; notebooks with Read, which shows cells and outputs). Note: the source's own
section structure, every worked example with its numbers, every table, every figure worth
reproducing, and any code (which will be translated to Julia).

### 2. Settle metadata and scope

Infer from the working directory and its git root: course code from a folder or repo
name like `DATA-5695-6695-Fall-2026` or `DATA 6690` (also check `syllabus/*.qmd`),
semester from the repo name, and the chapter number from the input. Look at any existing
deck in the same `slides/` folder and match its stem pattern, date style, and Part layout.

Ask **one** `AskUserQuestion` (at most three questions) only for things that change the
work materially and cannot be inferred: scope when the source is much bigger than a
lecture, the course when it cannot be found, and whether slides should quote a shared code
module that already exists in `code/`. Everything else is a routine call: make it, and
list it in the final report.

### 2b. Consult any reference document (optional)

A reference is any pre-existing treatment of the same material that is not the primary
source: an older deck of Tyler's (Beamer `.tex`, Rmd, PDF, PowerPoint), a set of lecture
notes, a notebook, a colleague's slides. One arrives via `--ref`, or an obvious one may sit
beside the input or in the "Earlier decks and notebooks" folders listed in
`reference/conventions.md`; mention a found one in the report rather than silently using it.

Read it in full and treat it as **advice from a previous run, not a template**:

- **Take from it**: the order in which topics are introduced, which examples and numbers
  were chosen for emphasis, intuitions and phrasings that teach well, pitfalls flagged for
  students, exercise ideas, and anything the primary source lacks that the reference adds
  usefully.
- **Do not take from it**: its format, theme, slide count, slide-by-slide structure, or
  code. The deck is still built from the primary source under the conventions in
  `reference/conventions.md`, with the usual Part layout, Road Map, Take Away and Exercises
  slides, and static Julia code with a check script. Python, R, or MATLAB in the reference
  is translated to Julia like any other source code, and its numbers are re-derived and
  checked.
- **Where they disagree**, the primary source wins on facts and numbers; the reference may
  win on pedagogy. Decide, do not blend, and list each such choice in the report.
- Without a reference, nothing changes: proceed as before.

### 3. Scaffold

```
python3 ~/.claude/skills/slides/scripts/new-deck.py --out slides --stem <stem> \
    --title "<Title>" --subtitle "<Source, Chapter N>" --course "<COURSE>" \
    --date "<Month YYYY>" --source "<one-line description of the input>"
```

This writes the `.qmd` (header from `assets/header.yml` plus a skeleton body), runs
`quarto add broughtj/quarto-usu-slides` in the deck folder if `_extensions/broughtj/usu-slides` is
missing (offline: `--ext-path ~/repositories/teaching/quarto-usu-slides`), writes
`check-<stem>.jl`, and creates or extends
the justfile at the git root (a fresh parameterized justfile, a new entry in an existing
`decks :=` list, or a namespaced `<stem>*` recipe block for a justfile with fixed names).
It refuses to overwrite an existing `.qmd` without `--force`.

### 4. Write the deck body

Replace the skeleton body. Follow `reference/conventions.md` exactly; the important
constraints are:

- Part standout headings, a Road Map slide, 15 to 30 content slides, Take Away and
  Exercises slides at the end.
- Only the portable constructs listed there. Nothing that works in HTML alone.
- Beamer fit limits: code lines at most about 85 characters, about 8 bullet lines, tables
  of at most 7 columns and about 10 rows, `{.smaller}` paired with a `{=latex} \small` block.
- Code is Julia, static, 5 to 15 essential lines per block, with its output quoted. If the
  material has a natural shared module (a type, a simulation), put it in `code/<name>.jl`
  so notes and slides quote one definition, and `include` it from the check script.
- Preserve the source's worked examples and numbers; do not invent data. Fix obvious
  typos in the source silently; note anything dropped or added.

Then fill `check-<stem>.jl` with one `expect` per quoted number.

### 5. Render and check

```
just deck <stem>          # or `just <stem>` when the justfile uses fixed names
just check <stem>         # or `just <stem>-check`
just verify <stem>
just sheet <stem>
```

Read `build/<stem>-sheet.png`. Rasterize suspect frames with `just page <stem> N` and read
them. Fix overflow, collisions, and orphans; re-render; repeat until clean. Do not report
done while the check script fails or a frame overflows.

### 6. Report

State where the outputs are, the Beamer page count, which checks ran and passed, and
every judgment call (scope trimmed, content reorganized, source errors corrected, naming
changes). If a reference document was used, say in two or three lines what was borrowed
from it and what was deliberately not. Do not commit unless asked. If the deck lives in a git repo, name the paths
`git status` will show.

## Files

| Path | Role |
|---|---|
| `assets/header.yml` | The 22-line front matter with `{{PLACEHOLDERS}}`. Formats are `usu-slides-revealjs`, `usu-slides-beamer`, `usu-slides-typst`. |
| (extension) | The theme itself (Beamer palette and title page, `slides.scss`, Typst page setup) lives in github.com/broughtj/quarto-usu-slides, local checkout `~/repositories/teaching/quarto-usu-slides`. Change the look there, push, then `just theme` (or `quarto update`) in each deck folder. |
| `assets/check-template.jl` | Skeleton for `check-<stem>.jl`. |
| `assets/justfile.template` | Parameterized justfile for a folder with none (`just deck <stem>`, `check`, `verify`, `page`, `sheet`, `preview`, `theme`, `clean`). |
| `assets/justfile-block.template` | Namespaced recipes appended to a justfile that uses fixed recipe names. |
| `scripts/new-deck.py` | The scaffolder (step 3). |
| `scripts/sheet.py` | Tiles rasterized pages into one contact sheet (needs Pillow). |
| `reference/conventions.md` | Structure, allowed constructs, Beamer fit limits, code rules, review checklist. |

## Requirements on the machine

Quarto 1.5+ (Typst bundled), LuaLaTeX with the Metropolis theme, Fira Sans and Fira Mono
installed as system fonts, `just`, Poppler (`pdfinfo`, `pdffonts`, `pdftoppm`), Python 3
with Pillow, Julia for the check script, and network access (or a local checkout) the first
time the extension is installed in a folder. Rendering itself needs no Julia.
