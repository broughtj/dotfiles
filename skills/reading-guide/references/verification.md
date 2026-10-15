# The verification pass

This is what separates a reading guide from a summary. A summary restates; a
guide *checks*. Budget real time for this — on a 30-page technical article it is
worth an hour of tool calls.

The output is the guide's closing section, **"A note on the text."**

---

## The governing rule

**Three different kinds of claim, three different confidence levels, reported
separately and labelled.** Collapsing them is the main way this section goes
wrong.

| Kind | Basis | How to phrase it |
|---|---|---|
| **Print error** | You recomputed it, or the source contradicts itself | Flat and unhedged. "The correct value is 1/3." |
| **Conversion artifact** | Present in the `.md`, absent from the PDF | Explicitly *not* the author's fault |
| **External check** | Depends on a fact outside the document | Give the reasoning so the reader can judge |
| **Reconstruction** | Your best explanation of an anomaly | "Offered as a reconstruction rather than a certainty" |

Never report a conversion artifact as an author's error. Always open the PDF and
confirm the anomaly is in the print before calling it a print error.

---

## What to check

### Recompute everything you can

Every number in a table, every worked example, every claimed limit. Use Python.
Specifically:

- **Do the totals add?** Row and column sums in every table.
- **Do the "theoretical" or "expected" values reproduce** from the formula the
  paper gives? If they do, you have validated both the formula and your reading
  of it. If they don't, work out the multiplier or convention the paper omitted
  before concluding it is wrong — the omission is itself worth reporting.
- **Do the reported statistics reproduce?** $p$-values, test statistics,
  posterior probabilities. Figure out the convention (e.g. a $\pm\tfrac12$
  continuity correction) from the rows that *do* reproduce, then apply it to the
  ones that don't.
- **Do the derivations hold?** Redo them independently. Where a stated result
  disagrees with the source's own displayed formula, that is a print error and
  you can say so flatly.
- **Are the asymptotics right?** Check claimed growth rates with Stirling or a
  quick numeric limit.

Add value the source didn't: if simulation results are compared to theory, compute
the **standard error** so "substantial agreement" can be quantified.

### Check the source against itself

- **Internal cross-references.** "See Tables 2–5" when only 2–3 apply. "See [52]"
  pointing at the wrong reference. These are common and easy to catch: pull every
  bracketed citation and check the name in the text against the reference list.
- **Name spellings** between text and reference list.
- **Numbering.** Volume/year pairs in a reference list are internally
  constrained: if four citations to the same journal fix the mapping
  (volume = year − N), a fifth that breaks it is wrong. **This is an internal
  check and can be stated confidently** — show the reasoning.
- **Sentences that don't finish.** Page breaks in scanned journals sometimes eat
  the end of a sentence. Read across every page boundary in the text layer.
- **Arithmetic in prose.** "1,250 for 500 predictions" when the design implies
  5,000.

### Check terminology and translation

For humanities texts: reference numbers (Stephanus, Bekker, chapter-and-verse),
transliterations, and quoted passages against the original where the source
provides it.

---

## How to find things

```bash
# printed-page-aware search of the PDF text layer
python3 ~/.claude/skills/reading-guide/scripts/pagemap.py find SOURCE.pdf 'PATTERN' -C 2

# confirm an anomaly is in the print, not the conversion
python3 ~/.claude/skills/reading-guide/scripts/pagemap.py find SOURCE.pdf 'the value of p is'

# pull every bracketed citation for cross-checking
grep -oE '\[[0-9]+(,[0-9 ]+)*\]' source.md | sort -u
```

Recompute in Python rather than by hand — it is faster and it does not make
arithmetic slips of its own.

---

## Reporting

Open with what **held**, not what broke. A positive verification is a finding,
and it tells the reader how much to trust the rest:

> Every total in Tables 2 and 3 adds up; every "theoretical" entry reproduces
> exactly from the §6 formula; every number in the Series B′→B paragraph
> reproduces. **It is the prose cross-references, not the computations, that
> slip.**

Then the errata as a three-column table — location, printed, should be — ordered
by how much they matter, not by page. A wrong correlation coefficient goes above
a misspelled name.

Then the hedged material under its own subheading, then conversion artifacts
under theirs.

### Calibration

- If an error changes nothing downstream, **say so**. "Nothing downstream depends
  on the number" is reassuring and true.
- If you cannot reconstruct an anomaly, report it as an anomaly rather than
  inventing an explanation: "the one entry that does not reproduce under the
  convention that fits the other sixteen."
- Don't pad the list. Three real findings beat fifteen with ten typos in them —
  though genuine typos in a scanned text are worth a compact tail-end list since
  they signal to the reader what else to distrust.
- **Never fabricate a correction.** If you are not sure the source is wrong, you
  do not have a finding. The whole section's value rests on the reader being able
  to trust it without re-checking.
