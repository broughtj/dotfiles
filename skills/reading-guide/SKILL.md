---
name: reading-guide
description: Produce a CliffsNotes-style reading guide to a paper, book chapter, or run of chapters — governing claim, section-by-section walkthrough, glossary, common misreadings, discussion questions, and a verified errata note — delivered as Markdown beside the source, a published Artifact, and a Quarto document rendered to HTML/PDF/DOCX. Use when asked for a "reading guide", "CliffsNotes style guide to the readings", "study guide", "guide to the reading", or structured reading notes on a specific document.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill, Artifact, SendUserFile, AskUserQuestion, Agent
---

# Reading Guide

## Purpose

Turn a dense source — a journal article, a book chapter, a run of chapters —
into a guide that does what a good teacher does: state the thesis before the
detail, walk the argument section by section, name the traps, and hand back the
apparatus (glossary, key results, questions) that makes the source re-readable.

The guide is not a summary. A summary tells you what the text says. This tells
you **what the text is doing, where it is strongest, where it slips, and what to
watch for** — and it backs that up by independently checking the source's own
arithmetic and citations.

## When to activate

- `/reading-guide <path>` or `/reading-guide <path> --chapters 2-5`
- "Make me a CliffsNotes style guide to the readings for X"
- "Do the same for this paper" (after a previous guide)
- "Reading guide / study guide / reading notes for <document>"

## Arguments

| Form | Meaning |
|---|---|
| `<path>` | The source. A `.md` conversion, a `.pdf`, or a folder holding both. |
| `--chapters 2-5`, `--sections 1-4` | Which part of a long source to cover. |
| `--no-artifact`, `--no-quarto` | Skip a deliverable for this run. |
| `--kennedy` | Restructure the walkthrough into Kennedy's three strata — body, General Notes, Technical Notes. See `references/kennedy-mode.md`. |
| `--pairs-with "<citation>"` | Name the main text this guide supplements, e.g. `--pairs-with "Greene, Econometric Analysis 8e, ch. 4"`. Adds a "Paired with" block and re-aims the technical material at bridging to it. Works with or without `--kennedy`. |

**Every flag is optional and every default is off.** With no flags you get the
standard guide described in `references/structure.md` and all three deliverables.
Flags are also requestable in words — "Kennedy style", "with general and
technical notes", "split the intuition from the algebra" all mean `--kennedy`;
"as a companion to Greene" means `--pairs-with`. Honor the words as readily as
the flag.

If the source is a whole book, one guide per coherent run of ~100–150 printed
pages. Ask which chapters only if the user hasn't said and the book is long
enough that the answer changes the work; otherwise take the obvious unit (a
single chapter, a single paper, "the introduction and chapter 1").

## Workflow

### 1. Inventory the source

`ls` the folder. You are looking for three things:

- **A Markdown conversion** (OCR/Mathpix). Read this — it is the full text.
- **The PDF.** This is the *authority*. The `.md` is a conversion and carries
  its own errors; never report a conversion artifact as an error in the book.
- **Sibling files** — other papers by the same author, earlier guides, notes.
  These become the "Where this connects" section and are a large part of the
  value. Check for a previous `reading-guide-*.qmd` in the same folder or a
  sibling one: match its conventions exactly, **including whether it used
  `--kennedy`**. The mode is sticky per folder — a shelf guided in Kennedy style
  should stay that way without being asked again.

**If there is no Markdown conversion**, first check whether the PDF has a text
layer:

```bash
pdftotext -f 1 -l 5 SOURCE.pdf - | wc -c     # a few thousand chars = usable
```

A usable text layer is all you need — `scripts/pagemap.py` reads it directly.
If it comes back near-empty the PDF is an image scan, and you can make a
Markdown version yourself:

```bash
mpx convert SOURCE.pdf SOURCE.md             # needs `mpx login` first
```

This calls the Mathpix API, so it costs credits and is slow on a long book.
Convert only the part you are guiding, and only when there is no text layer.
Either way the **PDF stays the authority**: a conversion carries its own OCR
errors, and Greek subscripts and display math are where it fails first.

### 2. Read the whole thing

Read the source **completely** before writing a word. Not the abstract, not the
first and last pages. If it is long, read it in chunks, but read all of it. The
guide's authority comes from having actually read it; a guide built from skimming
is obvious to the reader and worse than none.

### 3. Build the page map

```bash
python3 ~/.claude/skills/reading-guide/scripts/pagemap.py map    SOURCE.pdf
python3 ~/.claude/skills/reading-guide/scripts/pagemap.py find   SOURCE.pdf 'PATTERN'
python3 ~/.claude/skills/reading-guide/scripts/pagemap.py extract SOURCE.pdf -o /tmp/src.txt
```

Every page reference in the guide must be a **printed** page number, the one the
reader sees. The script infers the physical→printed offset from running heads.
If the PDF has no text layer, say so and cite by section instead of page — do not
guess.

### 4. Verify

This is the step that makes the guide worth having. Read
`references/verification.md` and do the pass described there: recompute the
arithmetic, check internal cross-references, check the reference list against
itself, and separate what you find into **print errors**, **conversion
artifacts**, and **external checks** (each hedged differently).

Report what you verified even when everything holds — "every total adds up and
every theoretical entry reproduces" is a finding.

### 5. Write the Markdown guide

Read `references/structure.md` for the full anatomy.

**If Kennedy mode is on** — `--kennedy`, asked for in words, or inherited from a
previous guide in the folder — also read `references/kennedy-mode.md`. Its
section order replaces §4 of `structure.md`; everything else there still applies.
Start from `templates/guide-kennedy.md` rather than `templates/guide.md`.

Write to:

```
<source folder>/Reading Guide -- <Descriptive Title>.md
```

Use `$…$` LaTeX for math (it survives into Quarto unchanged).

### 6. Publish the Artifact

Load the `artifact-design` skill first, then write **HTML** (never Markdown — the
`.md` publish path won't render the LaTeX). Convert the math to Unicode/HTML.
Read `references/artifact.md` for the conversion notes and the design brief that
worked.

### 7. Build the Quarto document

Copy `templates/guide.qmd` — its YAML is the house style and should not be
re-derived. Read `references/quarto.md` for the callout mapping and the two
gotchas that will otherwise cost you a render cycle. Then:

```bash
cd "<source folder>" && quarto render reading-guide-<slug>.qmd
```

Check the render output for `WARNING`. Spot-check one math page and one table
page as PNGs (`pdftoppm -png -r 110 -f N -l N file.pdf out`) before declaring it
done — a broken glyph or a collapsed table only shows up visually.

### 8. Hand off

`SendUserFile` the `.qmd` and `.pdf`. In the reply, lead with **what you found**
— the errata, the checks that held, the connections to sibling files — not with
a description of the document's structure. The user can see the structure.

## Non-negotiables

These are what make the output good rather than generic:

1. **Thesis first.** The guide opens with the source's governing claim in a
   single block, then a table of what each section does *for that claim*. A
   reader who stops after the first screen should still have the argument.
2. **Verify, don't paraphrase.** Recompute. Catching a real error — a wrong
   correlation, a misprinted citation, a sentence lost at a page break — is the
   single highest-value thing in the guide.
3. **Report the source's own concessions.** Find the places where the author
   admits a limit, and quote them. Readers miss these; they are usually the most
   honest sentences in the text.
4. **Name the traps.** "Common misreadings to avoid" should list things a smart
   reader would actually get wrong, each with the correction.
5. **Be fair.** Where the argument is weak, say so plainly and once. Where it is
   strong, say that too. No hedging every sentence, no debunking.
6. **Distinguish certainty levels.** Verified-by-recomputation, internal
   inconsistency, and external check are three different claims. Label them.
7. **Cite by printed page** throughout.
8. **Write for a master's-level reader** — someone competent in the field who is
   meeting this material for the first time. Plain words, short sentences, terms
   glossed on first use. Simple language, not simplified content: the algebra and
   the disagreements stay. See the register section of `references/structure.md`.

## File naming

| Deliverable | Name |
|---|---|
| Markdown | `Reading Guide -- <Title>.md` |
| Quarto source | `reading-guide-<slug>.qmd` |
| Renders | `reading-guide-<slug>.{html,pdf,docx}` |
| Artifact title | A short specific noun phrase — `<Author> <Year> Reading Guide` |

All of them live **next to the source**, not in a scratch directory.

## Reference files

| File | Read it when |
|---|---|
| `references/structure.md` | Writing the guide — the full section-by-section anatomy |
| `references/kennedy-mode.md` | Step 5, only under `--kennedy`/`--pairs-with` — the three strata and what goes in each |
| `references/verification.md` | Step 4 — the checking discipline and how to report |
| `references/quarto.md` | Step 7 — YAML, callouts, and the gotchas |
| `references/artifact.md` | Step 6 — HTML conversion and design brief |
| `templates/guide.qmd` | Step 7 — copy this, don't re-derive the YAML |
| `templates/guide.md` | Step 5 — the Markdown skeleton |
| `templates/guide-kennedy.md` | Step 5 — the Markdown skeleton, Kennedy mode |
| `scripts/pagemap.py` | Step 3 — printed-page extraction and search |
