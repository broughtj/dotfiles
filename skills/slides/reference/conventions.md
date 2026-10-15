# Deck conventions

Rules distilled from the DATA 6690 probability deck and the DATA 5695/6695 futures
mechanics deck. One `.qmd` renders to revealjs HTML, a Beamer PDF (Metropolis, navy
palette, Fira fonts), and a Typst handout through the `usu-slides` Quarto extension
(`_extensions/broughtj/usu-slides` beside the deck; source at github.com/broughtj/quarto-usu-slides).
Theme changes go in the extension, never in a deck's front matter. **Beamer is the primary deliverable**; if a
construct works only in HTML, do not use it.

## Structure

- Title slide comes from the YAML. Then `# Part N: Title {background-color="#1B2A4A"}`
  level-1 headings; each becomes a navy standout frame in Beamer and a navy slide in HTML.
  Three to six Parts.
- Second slide is a **Road Map** table: `| Part | Topic | Source |`.
- `##` headings are slides. Aim for 15 to 30 content slides per lecture; 2 to 4 per Part
  minimum. One idea per slide, title states the idea ("Margin Call Tops Up to Initial",
  not "Margin Calls").
- Close with **What to Take Away** (two columns: concepts / machinery), **Exercises**
  (3 to 7 numbered items pointing at the source), optionally **Further Reading**, and a
  final `::: {.fragment} **Questions?** :::`.

## Portable constructs (the whole allowed list)

- `::: {.columns}` with `::: {.column width="50%"}` (also 40/60, 60/40).
- `::: {.fragment}` for progressive reveal. Beamer and Typst ignore it gracefully.
- Callouts, always `appearance="minimal" icon="false"`: `.callout-tip` for the
  takeaway, `.callout-note` for asides and definitions, `.callout-warning` sparingly.
- Blockquotes for quotations, attribution on its own line: `> — Author, §x.y`.
- Pipe tables. Keep to 7 columns or fewer for Beamer; numeric columns right-aligned;
  bold a highlighted row. Short header labels (Typst hyphenates long ones badly).
- Images: `![](figs/name.png){width=56%}`. Figures live in a `figs/` folder beside the deck.
- Fenced code: plain ```` ```julia ````, never `{julia}`. Code is not executed on slides.
- Math: `$...$` and `$$...$$`. Number equations inside the math as `\qquad (2.5)`;
  `\tag` does not survive Typst. Bold vectors use `\mathbf{}`; the header routes it
  through `\symbf` for LuaLaTeX.
- Size control: put `{.smaller}` on the slide heading **and** a ```` ```{=latex} \small ``` ````
  block right under it. `.small`/`.smaller` classes only reach the HTML deck.
- `::: {.small}` or `::: {.muted .small}` for footnote-like lines (HTML only; harmless elsewhere).
- Upright labels in math (`PV`, `Div`, `Eur`, `Amer`): write `\text{PV}`, not `\mathrm{PV}`.
  Under LuaLaTeX `\mathrm` pulls Latin Modern Roman into the PDF and `just verify` flags it;
  `\text` uses Fira Sans and survives Typst and MathJax.
- Currency amounts in prose: escape the sign, `\$40`. A bare `$40 ... time-$T$` pairs the
  first `$` with the next one and swallows the sentence into math. Inside code blocks `$` is
  literal and needs no escape.
- Pipe-table column widths follow the dash counts in the separator row once any row is
  long. Give a label column more dashes than the numeric ones or Beamer wraps "Buy four
  50-strike calls" onto two lines.

Do not use: `::: {.incremental}`, `{.scrollable}`, absolute positioning, speaker notes,
HTML tags, `\tag`, `{{< include >}}`, executed code cells, tabsets, or any revealjs plugin.

## Fitting Beamer frames (10pt, 16:9)

- Code lines: **at most about 85 characters** including indentation, or they run off the
  right edge. Break long expressions into named intermediates; prefer a multi-line `if`
  over a long ternary. Code block plus a one-line caption: at most about 16 lines. Two
  code blocks on one frame: at most about 8 lines each.
- Bullets: at most about 8 lines of rendered text per frame; each bullet one line, two
  at most. Split rather than shrink.
- Tables: about 10 body rows fits with a short caption; 12 with `{.smaller}` + `\small`.
- Columns: each column at most about 6 short lines.
- Comment columns in struct listings: keep the comment short enough that the longest
  line stays under the 85-character limit.

## Code on slides

- Language is Julia unless the course is explicitly something else. Translate source
  material's Python/MATLAB/R to idiomatic Julia (`mutable struct` + `update!` for a
  class, `diff`/`cumsum` for NumPy, Distributions.jl for scipy.stats).
- Show **the essential 5 to 15 lines**, not whole files. Quote the output as a comment
  (`# [100.0, 150.0, -200.0]`) or a bold number in the prose right under the block.
- If the code lives in a shared module (e.g. `code/m2m.jl` that the notes also `include`),
  the slide quotes the same lines verbatim; the check script `include`s the module.
- **Every quoted number goes into `check-<stem>.jl`** as an `expect(...)` and the script
  must pass before the deck is reported done. Numbers copied from a textbook get the book
  value as `want` with a tolerance matched to the book's rounding.

## Metadata

- `title`: short noun phrase (2 to 5 words). `subtitle`: source and chapter, e.g.
  "Hull, Chapter 3" or "Martinez & Martinez, Chapter 2".
- `institute`: course code on the first line (`DATA 5695 / 6695`, `DATA 6690`), then
  "Data Analytics & Information Systems, Utah State University". Infer the course from the
  repository or folder name; ask only if it cannot be inferred.
- `date`: month and year of the lecture, e.g. "October 2026".
- File stem: `chNN-topic` with a two-digit chapter number and a two-to-three-word slug.

## Review before reporting

1. `just check <stem>` (or `just <stem>-check`) passes.
2. `just verify <stem>`: expected page count, fonts are Fira Sans / Fira Mono / Latin
   Modern Math only, no external `src=` in the HTML.
3. `just sheet <stem>`, then **read the contact sheet image** and look for: code or
   tables running off the right edge, frames that overflow the bottom, orphaned
   headings, empty-looking frames, callouts cut in half.
4. Rasterize any suspect frame with `just page <stem> N` at 110 dpi and read it.
5. Fix and re-render until clean. Report the page count, the checks that ran, and every
   judgment call (content dropped, renamed, or added beyond the source).

## Using a reference document

When a prior deck or set of notes on the same material is supplied (`--ref`) or found,
it informs *what to emphasize and in what order*; it never overrides anything above.
Format, Part layout, portable constructs, Beamer fit limits, Julia code, and the check
script stay exactly as specified here. Borrow the reference's good examples, framing, and
exercises; re-derive its numbers from the primary source and put them in `check-<stem>.jl`;
translate any of its code to Julia. Record in the report what came from the reference.

## Where source material lives

- Hull, *Options, Futures, and Other Derivatives*, **11th edition**, one text-layer PDF per
  chapter: `~/Library/CloudStorage/GoogleDrive-broughtj@gmail.com/My Drive/Books/O/Options,
  Futures, and Other Derivatives/11th Edition/Chapter NN - <title>.pdf`. Use this edition for
  every Hull deck unless told otherwise; `pdftotext -layout` gives clean text. The 8th
  edition scans in `8th Edition/` and in the Fin 5330 repo are older and image-only.
- Other textbooks: look under `.../My Drive/Books/<first letter>/<title>/` first.
- McDonald, *Derivatives Markets*, **3rd edition**: chapter PDFs and the publisher's
  lecture-note PDFs (`LN09McD...ppt.pdf`) live in `references/McDonald/` of the DATA 5690/6690
  repo. The LN deck is a reference for emphasis (`--ref`), not a source.
- Earlier decks and notebooks worth mining: `~/repositories/teaching/Fin6470/` and
  `~/usu/teaching/Previous/` (Beamer via Rmd, 2020 to 2021).
