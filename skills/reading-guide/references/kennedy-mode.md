# Kennedy mode

Peter Kennedy's *A Guide to Econometrics* is built to be read **beside** a main
textbook, not instead of one. Its chapters stratify by register rather than by
topic: the same material gets three passes at increasing technical depth, so a
reader can take the intuition front-to-back and come back for the apparatus.

This file replaces **§4 (Section-by-section walkthrough)** of `structure.md`.
Everything else there — the governing claim, the notation table, the study
apparatus, the register, the length ratio — still applies unchanged.

Fires when the user passes `--kennedy`, asks for the mode in words ("Kennedy
style", "with general and technical notes", "split the intuition from the
algebra"), or when a previous guide in the same folder used it.

---

## The three strata

| Stratum | Holds | Kennedy's own rule |
|---|---|---|
| **Body** (§N.1, §N.2 …) | The mechanism, verbally. What is going on and why it matters. | *"an intuitive feel for its concepts and techniques, without the usual clutter of notation and technical detail"* |
| **General Notes** | Literature, controversy, practice, terminology, quotable lines, cross-references | *"All references, peripheral points, and details worthy of comment are relegated to a section at the end of each chapter"* |
| **Technical Notes** | The formula, the derivation, the condition, the proof sketch | *"supplements rather than duplicates the contents of traditional textbooks … a useful introductory bridge to the more sophisticated presentations found in their main text"* |

### The rule that makes it work

**No footnotes, no parenthetical asides in the body.** This is the discipline
Kennedy states in the preface and it is what keeps the body readable. If you
want to say something and the argument does not need it, it goes down a
stratum. There is no third option.

The body is not a summary of the notes and the notes are not an appendix to the
body. They are the same argument at three magnifications.

## Where a given point goes

Ask in this order:

1. **Would a reader who never opens the notes still get the argument without
   it?** If yes, it is not body material. Push it down.
2. **Can it be stated without notation?** If no, Technical Notes.
3. **Otherwise, General Notes.**

| Goes in the **body** | Goes in **General Notes** | Goes in **Technical Notes** |
|---|---|---|
| Why the problem arises at all | Who established it and where | The estimator, written out |
| What goes wrong, in words | Where the field still disagrees | The derivation, or the step the main text skips |
| The decision the practitioner faces | Rules of thumb — and why to distrust them | Regularity conditions, and what breaks without them |
| A named picture (the Ballentine, a confidence ellipse) | Why the thing is *called* that | Asymptotic argument, order of magnitude |
| One quotable line, if it *is* the point | Software defaults and their traps | Notational translation between conventions |
| | Pointers to other chapters | |

Author names appear in the body only where the name **is** the concept ("the
Ballentine", "a Koyck lag") or where a sentence is worth quoting for its own
sake. A name attached to a claim is a literature pointer and belongs one
stratum down.

## Section order

Per chapter or coherent unit:

```markdown
# Chapter N: <Title>

## N.1 <Section title>            <- body: intuition only
## N.2 <Section title>
## N.3 <Section title>

## General Notes {.unnumbered}
### N.2 <Section title>           <- keyed to the body sections
### N.4 <Section title>

## Technical Notes {.unnumbered}
### N.2 <Section title>
```

The numbers shown in the body headings above are for the **Markdown**
deliverable. In the `.qmd`, strip them and let Quarto number — see the numbering
note in `quarto.md`. The General/Technical sub-keys keep their numbers in both,
because those headings are `{.unnumbered}` and nothing else would supply them.

Both notes sections are **keyed by section number**, and only sections that
earned notes appear. In Kennedy's chapter 12 the General Notes run 12.2, 12.3,
12.4 — §12.1 gets none, because an introduction that only sets up the problem
has nothing peripheral to relegate.

Three rules follow:

- **A stratum with nothing in it is omitted, not padded.** Kennedy's chapter 7
  has General Notes and no Technical Notes at all. Inventing three thin bullets
  to fill the heading is worse than the heading's absence.
- **Drop the `###` sub-keys when the stratum is short.** Chapter 12's Technical
  Notes are four bullets with no subheadings. Below roughly six bullets, key
  each one inline instead — *"**§12.2.** The estimated variance is …"*
- **Notes are bulleted, not prose.** Each bullet is one self-contained point.
  This is what makes the stratum scannable and what lets a reader jump straight
  to the note for the section they are stuck on.

## Proportions

Across Kennedy's chapters the body runs roughly 30–55% of the whole, and the two
notes sections together usually **equal or exceed** it. Chapter 19 spends 8
printed pages on the body and 27 on the notes; chapter 22 inverts it.

Use that as a diagnostic rather than a target. If your Technical Notes come to
three bullets, the body is almost certainly carrying algebra it should have
handed down. If your body has shrunk to a page, you have written an annotated
bibliography.

## Pairing with a main text

`--pairs-with "<citation>"` names the textbook this guide supplements — e.g.
`--pairs-with "Greene, Econometric Analysis 8e, ch. 4"`. It is usable with or
without `--kennedy`, but the two together are the intended shape.

When it is set:

- Add a short **Paired with** block after the title, before the governing claim:
  the main text's corresponding sections, and the reading order between them
  (usually: this guide's body → the main text → this guide's notes).
- Add a **Main text** column to the governing-claim table, mapping each section
  to where the same ground is covered there.
- **Re-aim the Technical Notes at the bridge.** They stop being a compressed
  textbook and become the step the main text skips: the scalar version of a
  result it gives in matrices, the reason its derivation takes the route it
  takes, the notational collision between the two sources. Kennedy's phrase is
  the standard — *supplements rather than duplicates*.
- Flag collisions explicitly. Two sources that use $k$ for different things is
  the single most expensive thing you can leave unsaid.

Without the flag, Technical Notes are self-contained: state the result, then
give the reader enough to reconstruct it.

## What moves out of the standard apparatus

Kennedy mode absorbs parts of `structure.md`'s Study Apparatus. Do not write
them twice.

| Standard section | In Kennedy mode |
|---|---|
| *Derivations worth doing yourself* | Into **Technical Notes**, keyed by section |
| *Where this connects* — the citation-to-sibling-file table | Into **General Notes**, keyed by section |
| *Key results / passages to mark* | Stays top-level; it is an index across the whole guide |
| *Common misreadings* | **Stays top-level.** Misreadings usually span sections, and it is the skill's own value-add — Kennedy has no equivalent |
| *A note on the text* | **Stays top-level.** It reports your verification pass, not the source's content |
| *The argument in one page*, *Glossary*, *Questions* | Unchanged |

## Register, per stratum

The master's-level rule in `structure.md` applies throughout. Each stratum then
narrows it.

**The body** is the one that changes most, and it is the plainest thing in the
guide. Short sentences. No hedging about what the literature thinks, no "note
that", no defensive qualification. Gloss each term as it arrives. Say the thing.

**General Notes** can be opinionated in a way the body cannot — this is where a
judgment like *"neatly summarized by Williams: the worth of a textbook tends to
be inversely related to the technical material devoted to multicollinearity"*
belongs. Quote generously; it is the stratum built for it. Keep your own
sentences plain even when the quotations are ornate.

**Technical Notes** are terse. State the result, say what it shows, stop. Define
every symbol you use, once, even if the body already met it — a reader arriving
here from the main text has not read the body. If a formula yields three
readable consequences, number them: Kennedy closes chapter 12 that way and it is
the most useful paragraph in the chapter.
