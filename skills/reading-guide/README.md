# reading-guide

Produces a CliffsNotes-style reading guide to a paper, chapter, or run of
chapters, in three forms: Markdown beside the source, a published Artifact, and a
Quarto document rendered to HTML / PDF / DOCX.

## Use

```
/reading-guide "path/to/paper.pdf"
/reading-guide "path/to/book folder" --chapters 2-5
/reading-guide "path/to/paper.md" --no-artifact
/reading-guide "Kennedy 6e" --chapters 12-13 --kennedy
/reading-guide "chapter.pdf" --kennedy --pairs-with "Greene, Econometric Analysis 8e, ch. 4"
```

All flags are optional and all default to off.

Or just ask: *"make me a CliffsNotes style guide to the readings for X."*

Point it at a folder when the source has both a `.pdf` and an OCR `.md` — it
reads the Markdown for content and uses the PDF as the authority for anything it
reports as an error.

No `.md` in the folder is fine. Most PDFs have a text layer, which is all
`pagemap.py` needs. For an image-only scan the skill can build one with
`mpx convert SOURCE.pdf SOURCE.md` (Mathpix — needs `mpx login`, costs credits,
slow on a long book).

## What comes out

```
<source folder>/
  Reading Guide -- <Title>.md          archival / Obsidian
  reading-guide-<slug>.qmd             Quarto source
  reading-guide-<slug>.html            self-contained, no sidecar directory
  reading-guide-<slug>.pdf             Palatino, ~1 page per 1.5 pages of source
  reading-guide-<slug>.docx            native OMML math, editable in Word
```
plus an Artifact URL.

## What's in the box

| Path | |
|---|---|
| `SKILL.md` | The workflow |
| `references/structure.md` | Anatomy of a guide, section by section |
| `references/kennedy-mode.md` | The three strata, and what goes in each |
| `references/verification.md` | The checking pass — how to catch and report errata |
| `references/quarto.md` | YAML, callouts, and the two gotchas |
| `references/artifact.md` | HTML conversion and design brief |
| `templates/guide.qmd` | Copy this; the YAML is settled house style |
| `templates/guide.md` | Markdown skeleton |
| `templates/guide-kennedy.md` | Markdown skeleton, Kennedy mode |
| `scripts/pagemap.py` | Printed-page-aware PDF extraction and search |

## Kennedy mode

`--kennedy` restructures the walkthrough the way Peter Kennedy's *A Guide to
Econometrics* structures its chapters: the same material at three
magnifications rather than one pass mixing them.

| | |
|---|---|
| **Body** | The mechanism, verbally. No citations, no algebra, no asides. |
| **General Notes** | Literature, controversy, rules of thumb, terminology, quotable lines. Keyed by section. |
| **Technical Notes** | The formula, the derivation, the condition. Keyed by section. |

The point is that a reader can take the intuition front-to-back and come back
for the apparatus. It suits a source you are reading *alongside* a main
textbook, which is what `--pairs-with` is for — it re-aims the Technical Notes
at bridging to that text rather than compressing it.

Kennedy's own discipline, worth keeping: no footnotes. Anything peripheral gets
relegated, which is what keeps the body readable.

The mode is sticky per folder — once one guide in a directory uses it, later
ones inherit it without being asked.

## pagemap.py

Standalone, useful on its own. Journal scans never start at physical page 1, so
this infers the offset from the running heads and lets you cite what the reader
actually sees.

```bash
python3 scripts/pagemap.py map     paper.pdf            # physical -> printed
python3 scripts/pagemap.py find    paper.pdf 'Theorem'  # search, reports p.NNN
python3 scripts/pagemap.py extract paper.pdf -o out.txt # text with page markers
python3 scripts/pagemap.py map     paper.pdf --offset 481   # override inference
```

Needs `pdftotext` (`brew install poppler`). If a PDF has no text layer the script
says so rather than guessing.

## Requirements

- `pdftotext` and `pdftoppm` — poppler
- `mpx` — optional, only for image-only scans with no text layer
- `quarto` and `xelatex` — for the Quarto deliverable
- Palatino, Helvetica, Menlo — standard on macOS

## Design notes

Guides are written for a **master's-level reader**: plain words, short sentences,
terms glossed on first use. That is a rule about prose, not about depth — the
algebra, the errata, and the disagreements all stay in.

The thing that makes these guides worth having is the **verification pass**:
recomputing the source's arithmetic, checking its internal cross-references, and
reporting what holds as carefully as what breaks. It is also the slowest step.
If you're ever tempted to skip it, produce a summary instead and call it one.

The three deliverables are not redundant. The Markdown is what gets searched and
linked from notes; the Artifact is what gets read on a phone and sent to someone;
the PDF is what gets annotated. They are generated from the same content, so
regenerating one means regenerating all three.
