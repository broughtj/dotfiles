# The anatomy of a reading guide

Follow this order. It does real work: the guide moves from *the one thing to
know*, through *the argument as it actually runs*, to *the apparatus that makes
the source re-readable*.

Every heading below appears in the finished guide. Skipping one is a decision,
not an oversight — and "Common misreadings" and "A note on the text" are the two
that most distinguish this from a summary, so skip them last.

The one sanctioned departure is **Kennedy mode** (`--kennedy`), which replaces §4
below with three strata and pulls two apparatus sections up into them. Everything
else on this page survives it unchanged. See `references/kennedy-mode.md`.

---

## 1. Title block

```markdown
# Reading Guide: <Author>, <Title>

**<Subtitle or the chapters covered>** · <full citation, one line>

---
```

For a book, name the chapters covered. For an article, give journal, volume,
year, pages, and anything about the occasion (a conference talk, a symposium
contribution, an invited comment) — provenance changes how a piece should be
read.

## 2. The Governing Claim (read this first)

The single most important section. Structure:

1. One line of setup: "Everything in the article serves one thesis:"
2. **The thesis in a blockquote**, in your own words, compressed to 2–4 lines.
   Not a quotation — a distillation. This is the hardest sentence in the guide
   and worth several attempts.
3. **Corollaries** — one to three numbered claims that carry the argumentative
   weight, each with why it matters.
4. **A table**: one row per section/chapter, columns for section, pages, and
   *the job it does for the thesis*. Not "what it says" — what it *does*.
5. **The hinge** — one paragraph naming the joint the whole thing turns on, and
   a recommendation of which two sections to read if only two.

## 3. Notation (technical sources only)

A table of every symbol, **with collisions flagged in bold**. Papers reuse
letters; readers lose an hour to it. Close with the single most useful mnemonic
you can extract (for Hill 1994: "*a* is the world, *b* is you").

Skip for humanities texts; there, fold key terms into the glossary instead.

## 4. Section-by-section walkthrough

> Under `--kennedy`, this section is replaced wholesale by the three strata in
> `references/kennedy-mode.md`. Read that instead; §§1–3 and 5 below still hold.

One `#`-level heading per section or chapter of the source, in order, numbered to
match the source's own numbering wherever possible.

Within each:

- **`## In one paragraph`** — a dense, complete summary. Someone who reads only
  these should be able to follow the argument end to end.
- **`## § <topic>` subsections** — the substance. Lead each paragraph with a
  **bolded phrase** naming what the paragraph is doing: *The complaint is about
  representability, not fit.* / *Why not model the events?* / *The key structural
  claim.* This is what makes a long guide scannable.
- **Quotations** where the author says it better than you can, especially the
  concessions.
- **Display math or key formulas**, set off, with a note on what to read off
  them.

### The moves worth making inside a section

| Move | What it looks like |
|---|---|
| **True in one sense, false in another** | Quote a claim, then show the sense in which it holds and the sense in which it doesn't. Readers routinely take the wrong one. |
| **The shortcut the author didn't take** | If a result has a one-line derivation the source does the long way, give it. Fastest route to real understanding. |
| **What drops out** | When a variable vanishes from a formula, say so and say why it matters. |
| **The author's own caveat** | Find it, quote it, and say what it costs the argument. |
| **The cleanest way to hold the contrast** | A small table reducing a long argument to two or three rows. |
| **Advertised but not used** | Note where a source develops machinery it then doesn't apply. |

## 5. Study Apparatus

A `#`-level heading, then these as `##` subsections:

### The argument in one page
A numbered list, one step per major move, each ending with a cross-reference to
where it happens. This is the guide's spine, extracted. Write it **last**, from
the finished walkthrough.

### Glossary of key terms
Two-column table: term, and *meaning as this author uses it*. That qualifier
matters — capture the author's idiosyncratic usage, coinages, and any term used
against its ordinary sense. Include foreign-language terms with transliteration.

### Key results / key passages to mark
Two-column table: page reference, and why it matters. For an argumentative text,
passages; for a technical one, results and equations. This is what the reader
annotates their own copy from.

### Derivations worth doing yourself (technical sources)

*Kennedy mode: these move into Technical Notes, keyed by section.*

Numbered, each a few minutes' work, each with the answer so the reader can check
themselves. Include at least one that **corrects the source** and one that
**reveals something the source doesn't remark on**. Six or seven is right.

### Common misreadings to avoid
Numbered, each: the misreading in quotation marks and bold, then the correction.
Seven to nine. These should be errors a *careful* reader would make — not
straw men. The best ones come from places where you nearly got it wrong.

### Questions for discussion
Numbered, genuinely open. Each should name the specific thing at stake and,
where possible, point at the page where the author leaves the question hanging.
Avoid questions with an obvious answer or that merely test recall.

### Where this connects / Where this leads

*Kennedy mode: the citation-to-sibling-file table moves into General Notes,
keyed by section. What is left here is "Where this leads".*

- **Within the folder**: a table mapping the source's own citations to files the
  user already has. Check the directory; this is high-value and cheap.
- **Reading order**: which sibling source to read first and why.
- **Threads opened here, paid off later**: for a book, which chapter resolves
  what.
- **Outside the folder**: the surrounding literature and the source's position
  in it.

### A note on the text
See `verification.md`. Three clearly separated groups — print errors, external
checks, conversion artifacts — plus a positive statement of what checked out.

---

## Register

**Write for a master's-level reader** — someone competent in the field who is
meeting this material for the first time. Think of a colleague who has read the
thing twice explaining what matters. That fixes the register:

- **Plain words, short sentences.** Prefer the ordinary word to the clever one.
  If a sentence needs two readings, split it.
- **Gloss terms on first use.** Any term the source introduces gets a one-line
  plain meaning the first time it appears, even though the glossary defines it
  again later. Do not assume the reader already has the vocabulary.
- **Direct.** "Read this carefully — it is true in a specific sense and false in
  another." Not "it may be worth noting that..."
- **No throat-clearing.** Every paragraph starts with its point.
- **Confident about the text, honest about uncertainty.** Where you're
  reconstructing rather than reporting, say "offered as a reconstruction rather
  than a certainty."
- **Plain judgment, not display.** A flat verdict is welcome — "this is the
  weakest step in the argument"; "the arithmetic is trustworthy, the prose
  cross-references slip." Ornamental phrasing is not. If a phrase is there for
  effect rather than for the reader, cut it.
- **Never condescend to the author or the reader.**

**Simple language is not simplified content.** The guide still does the algebra,
still names where the field disagrees, still reports what it verified. Plain
prose is how that material gets delivered, not a reason to carry less of it.

## Length

Proportional to the source, roughly 1 part guide to 4 parts source by word
count. A 30-page article → ~12,000 words. A 150-page run of chapters → longer,
but split into two guides before it exceeds ~20,000.
