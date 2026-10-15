# The Quarto deliverable

The `.qmd` is the archival and print form. Its YAML is settled house style —
copy `templates/guide.qmd` rather than re-deriving it.

---

## Two gotchas that cost a render cycle

**1. `@sec-` cross-references do not resolve to `{.unnumbered}` sections.**

Quarto's crossref filter only resolves refs to *numbered* sections. The Study
Apparatus and everything under it is unnumbered, so:

```markdown
See @sec-derivations.              <- WARNING: Unable to resolve crossref
See [derivation 4](#sec-derivations).   <- works in html, pdf, and docx
```

Use `@sec-` for the numbered walkthrough sections, plain links for anything in
the apparatus. The anchors exist either way; only the auto-numbering doesn't.

**2. Keep math in `$…$`, not bare Unicode.**

`ρ`, `∑`, `≈` typed as literal characters get looked up in **Palatino**, which
may not have them, and will silently fall back or drop. `$\rho$` is typeset by
Latin Modern Math and always works. This applies to prose too — `$m \to \infty$`,
not `m → ∞`.

Safe as literal characters in prose: accented Latin (Pólya, Poincaré), en/em
dashes, curly quotes. Everything mathematical goes in math mode.

---

## Structure

```markdown
# Before You Start {.unnumbered #sec-overview}     <- governing claim, notation

# Introduction {#sec-intro}                        <- numbered; matches source §§
## The event series {#sec-events}
### A sub-point                                    <- no id needed

# Study Apparatus {.unnumbered #sec-apparatus}
## Glossary of key terms {.unnumbered}
```

With `number-sections: true` and the overview unnumbered, Quarto's numbering
lands on 1, 2, 3… — so **if the source numbers its own sections, the guide's
numbering matches it for free**. Say so in the opening line; it is a real
navigational aid, not a coincidence to leave unremarked.

Put the page range under each heading as an italic line: `*Pages 483–485.*`

## Callouts carry the structure

| Callout | Job |
|---|---|
| `.callout-note title="In one paragraph"` | Opens every walkthrough section. Always this exact title. |
| `.callout-important` | The governing claim; the author's key stated claims; theorems worth boxing |
| `.callout-warning` | Traps, corrections, conversion artifacts, "Common misreadings" |
| `.callout-tip` | Verified checks, "mark this paragraph", derivation pointers |

```markdown
::: {.callout-note title="In one paragraph"}
Text.
:::
```

Give every callout a `title=`; untitled ones render as a bare icon and read as
an accident.

## Kennedy mode

See `references/kennedy-mode.md` for what the three strata are. Two things about
rendering them.

**Do not wrap a whole stratum in a callout.** General Notes routinely run longer
than the body they annotate; a ten-page tinted box is unreadable. The strata are
headings. Reserve callouts for individual items inside them:

| Where | Callout |
|---|---|
| A boxed result or formula in Technical Notes | `.callout-important title="..."` |
| A passage worth quoting in General Notes | `.callout-tip title="Worth quoting"` |
| A rule of thumb that should be distrusted | `.callout-warning title="..."` |

**The notes headings must be `{.unnumbered}`.** Otherwise `## General Notes`
under a numbered chapter renders as *12.5* and collides with the source's own
section numbering — which is exactly the navigational aid the numbering was for.
Being unnumbered, they take plain links rather than `@sec-` refs (gotcha 1).

```markdown
# Chapter 12: Multicollinearity {#sec-ch12}
## 12.1 Introduction {#sec-12-1}
## 12.2 Consequences {#sec-12-2}

## General Notes {.unnumbered #sec-gn12}
### 12.2 Consequences {.unnumbered}

## Technical Notes {.unnumbered #sec-tn12}
```

**Numbering a run of book chapters.** Quarto numbers by document order, so the
guide's chapter becomes section 1 whatever the source calls it. Two cases:

- **A guide to chapter 1 needs nothing.** Section 1 *is* chapter 1, so `##` lands
  on 1.4 and `###` on 1.4.2 — the guide's numbering reproduces the source's for
  free, provided you strip the source's numbers from the heading text and let
  Quarto supply them. Say so in the opening line; it is a real navigational aid,
  and it means `@sec-` refs read as the source's own section numbers.
- **Chapter 2 and up: put the numbers in the heading text.** A guide to chapters
  12–13 numbers them 1 and 2. `number-offset: [11]` looks like the fix and is a
  trap — **it applies in the HTML output and is ignored in the PDF**, so the two
  formats disagree and only the PDF is wrong. It also cannot cope with an
  unnumbered opening section (a chapter preamble before §N.1), which silently
  shifts every later number by one. Set `number-sections: false` and write the
  source's own numbers into the headings (`## 2.4 Formal Model Checks`). Verified
  on Lancaster ch. 2.

## Tables

Pipe tables with a caption line underneath:

```markdown
| Term | Meaning |
|---|---|
| ... | ... |

: Key terms {#tbl-glossary}
```

Right-align numeric columns with `|---:|`. Keep three-column errata tables to
short cells — at `margin=1.15in` on letter paper a wide table wraps hard.

## Render and check

```bash
cd "<source folder>" && quarto render reading-guide-<slug>.qmd
```

All three formats build from one command. Then:

```bash
# no unresolved crossrefs, no LaTeX errors
quarto render reading-guide-<slug>.qmd 2>&1 | grep -iE 'warning|error'

# fonts actually applied (expect Palatino, Helvetica, Menlo, LatinModernMath)
pdffonts reading-guide-<slug>.pdf

# html is genuinely self-contained (expect no output)
grep -oE 'src="https?://[^"]+"' reading-guide-<slug>.html | sort -u

# docx has real math, not images
python3 -c "import zipfile;print('<m:oMath' in zipfile.ZipFile('reading-guide-<slug>.docx').read('word/document.xml').decode())"
```

**Always look at a page.** Render one math-heavy page and one table page to PNG
and read them:

```bash
pdftoppm -png -r 110 -f 19 -l 19 reading-guide-<slug>.pdf /tmp/pg
```

A missing glyph, a collapsed table, or a callout icon that failed to load does
not show up in any of the text checks above.

## What the YAML gives you

- `embed-resources: true` — one self-contained `.html`, no sidecar `_files/`
  directory to keep in sync when the file moves in Drive.
- `theme: cosmo`, `max-width: 54em`, `linestretch: 1.6` — reading-length measure.
- `toc-depth: 3` in HTML, `2` in PDF — the PDF TOC stays one page.
- Palatino / Helvetica / Menlo — Palatino carries full polytonic Greek on macOS,
  which matters for classical sources. Georgia, Didot, and New York do **not**;
  swap with care.
- `colorlinks: true` with `linkcolor: RoyalBlue` — internal links visible in
  print without boxes.
