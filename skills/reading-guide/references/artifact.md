# The Artifact deliverable

The Artifact is the read-it-now, read-it-on-a-phone, send-it-to-a-colleague form.
It is the same content as the Markdown, re-typeset for the screen.

---

## Non-negotiable mechanics

**Load the `artifact-design` skill before writing the file.** Not optional — it
calibrates the design treatment.

**Author HTML, never Markdown.** A `.md` publish renders LaTeX as literal
`$…$`, takes its title from the filename, and skips the design pass entirely.
Write a `.html` file and pass that path to the Artifact tool.

**Convert the math.** The Markdown guide uses LaTeX; the artifact needs
Unicode/HTML, since there is no MathJax and the CSP blocks CDN scripts.

| LaTeX | HTML |
|---|---|
| `$Y_t$` | `<span class="m">Y<sub>t</sub></span>` |
| `$2^{-n}$` | `2<sup>−n</sup>` (U+2212 minus, not hyphen) |
| `$\binom{n}{r}$` | `C(n,r)` — state the convention once near the top |
| `$\to$`, `$\approx$`, `$\geq$` | `→`, `≈`, `≥` |
| `$$…$$` | a `.eq` block: monospace, `white-space: pre`, `overflow-x: auto` |

`white-space: pre` on display equations is what preserves multi-line alignment;
without it every equation collapses to one line.

**Never hand a display equation to pandoc.** If you build the page by running
the Markdown guide through pandoc, do *not* emit `<div class="eq">…</div>` into
the Markdown. Pandoc processes the contents of a raw HTML block, and multi-line
content does not survive it: the first line becomes a `<pre><code>` block and
the remaining newlines collapse to spaces, so **every stacked fraction loses its
alignment**. Four or more leading spaces on the tag's own line does the same to a
one-liner, and a blank line inside the block ends it early and escapes the
closing tag to `&lt;/div&gt;`.

Emit a bare alphanumeric token instead, and substitute after pandoc has run:

```python
EQS = []
def repl_display(m):
    EQS.append(DISPLAY[m.group(1).strip()])
    return "\n\nEQBLOCKZZ%dZZ\n\n" % (len(EQS) - 1)
md   = re.sub(r"\$\$(.+?)\$\$", repl_display, md, flags=re.S)
html = pandoc(md)
for i, eq in enumerate(EQS):                    # pandoc wraps a bare token in <p>
    tok = "<p>EQBLOCKZZ%dZZ</p>" % i
    assert html.count(tok) == 1
    html = html.replace(tok, '<div class="eq">' + escape(eq) + "</div>")
assert "EQBLOCKZZ" not in html
```

HTML-escape the equation text: display maths routinely contains `<`, as in
`T(y) < 0`.

**Tag balance will not catch this.** A mangled block is still well-formed HTML —
the page validates, publishes, and looks fine until you read an equation. The
check below therefore has to look *inside* the `.eq` blocks.

**Self-contained.** No external assets except Google Fonts. Inline all CSS.

**Publish with a favicon** and a one-sentence `description` — the description is
the gallery card's subtitle, so it carries the explanation the title shouldn't.

---

## The design brief that worked

Ground the identity in the *subject's own world* rather than in "academic paper."
For Hill 1994 — Pólya urns, coin flips, IBM stock — that meant:

- **Type**: IBM Plex Sans Condensed for headings and IBM Plex Mono for math and
  data (IBM being the paper's only real data set), against Spectral for reading.
  A condensed grotesque over a screen serif is a classic journal pairing and is
  not one of the AI-default looks.
- **Color**: carmine — the red ball in the urn — as the single accent, on a
  cool-neutral paper with a faint indigo bias. A muted teal used *only* for
  "verified."
- **Semantics in color**: this is the part worth copying. Carmine means *error or
  correction*; teal means *verified*. Do not use one accent for both "best score
  in this table" and "printed mistake" — the reader can't tell which they're
  looking at.

Structural devices should encode something true. Section numbers are fine here
because the source really is numbered; page ranges in the heading are real
information. Don't add 01 / 02 / 03 markers to something that isn't a sequence.

## Components worth having

| Component | Why |
|---|---|
| Thesis block | The governing claim, set larger with an accent rule |
| `.eq` block | Display math, scrollable, with an optional uppercase label |
| Callouts | Trap / correction / verified — mirrors the Quarto callout roles |
| Journal-style tables | No vertical rules, hairline horizontals, `tabular-nums` |
| Glossary as a `<dl>` grid | Two columns on desktop, stacked on mobile |
| Jump strip | A dozen section links under the masthead; the guide is long |
| Stratum bands (Kennedy mode) | A tinted full-bleed band behind General Notes and another behind Technical Notes |

Under `--kennedy` the page is the deliverable that benefits most: the three
strata are a visual idea, and on the web you can actually show them. Give
General Notes and Technical Notes each a distinct background band running the
full width, keep the body on the page's own ground, and set the notes one step
smaller. A reader should be able to tell which magnification they are at from
across the room. Add the two strata to the jump strip per chapter.

## Before publishing

```bash
# tag balance
python3 - <<'PY'
import re
s=open('guide.html').read(); b=s[s.index('<div class="wrap">'):]
for t in ['div','section','table','tr','td','th','ul','ol','li','p','span','dl','dt','dd']:
    o=len(re.findall(rf'<{t}(?:\s[^>]*)?>',b)); c=len(re.findall(rf'</{t}>',b))
    if o!=c: print(f'MISMATCH {t}: {o}/{c}')
print('stray LaTeX:', b.count('$'))
print('escaped tags:', b.count('&lt;/div&gt;'))
eqs = re.findall(r'<div class="eq">(.*?)</div>', s, re.S)
print('eq blocks:', len(eqs), '| mangled:',
      sum(1 for e in eqs if '<pre' in e or '<code' in e))
PY
```

All four counts must be zero: stray `$` means a math conversion was missed;
escaped tags and tag mismatches mean a raw block was broken; **mangled eq blocks
mean pandoc ate the equation layout**, which nothing else here detects. Also eyeball
one stacked fraction in the published page — that is the only way to be sure the
alignment survived.

## Title

A short specific noun phrase, two to four words, that identifies the page in a
gallery of dozens: `Hill 1994 Reading Guide`. Not a category label
(`Reading Guide`), not a name with an explainer appended after a dash. Keep it
and the favicon stable across redeploys.

## Updating

Republish the **same file path** in the same conversation to keep the URL. From a
different conversation, pass the artifact's `url`. Publishing without it creates
a second artifact instead of updating the first.
