# socrates-write

A Socratic writing session. Claude plays Socrates and makes you write a section
of a paper yourself, one paragraph at a time. It is the sibling of `socrates`:
that skill tests whether you understood a reading; this one makes you say, in
your own sentences, what your own section has to say.

Socrates never drafts or rewords your prose. He asks what the paragraph is for,
what it claims, what the claim rests on, and what a hostile referee will say.
You write it. He tests it by questions and checks every quotation against the
source. When it passes, it goes into the file exactly as you wrote it.

## Use

```
/socrates-write sections/02-some-section.qmd --guide notes/study-guide-section-2.qmd
/socrates-write sections/02-some-section.qmd --part 2.3
/socrates-write draft.md --reference archive/old-draft.md --gentle
```

| Flag | Effect |
|---|---|
| `--guide <path>` | The study guide or outline that says what each part must answer, with sources and pages. |
| `--part <id>` | Start at a given subsection or TODO. Default: where the writing log says the last session stopped. |
| `--reference <path>` | An earlier draft Socrates may point you to when you are stuck. He never pastes from it. |
| `--gentle` | More scaffolding. Default is firm. |
| `--no-log` | Skip the writing log. |

## How a session goes

1. Socrates reads the section file, the guide, the project's writing rules, the
   prose already accepted, and the pages you will quote.
2. For each paragraph: he questions you until you can state its claim, its
   support with a page, and why it comes where it does. Then he says "write it."
3. You write the paragraph.
4. He tests it: its job, one claim, your words, support on the page, quotations
   exact, the reader. Failures come back as questions, not corrections.
   Quotation mismatches come back as facts.
5. Accepted paragraphs are placed verbatim. Typos and style items are listed
   for you to fix or leave.
6. At the end, a writing log records what was accepted, the decisions you made
   in your own words, and where to start next time.

Say "I'm stuck" to narrow the question, "point me to the text" for a page, and
"stop here" to end the session.

## What it needs

A section file with a plan in it (TODO comments are ideal) and, for best
results, a guide that states the questions each part must answer and gives the
sources with pages. Without a guide Socrates works from the TODOs alone and
says so.

## Install

Symlink or copy this folder into your agent's skills directory, as for
`socrates`:

```sh
ln -sfn ~/repositories/dotfiles/skills/socrates-write ~/.claude/skills/socrates-write
```

The conduct rules are Ward Farnsworth's "Socratic Rules of Engagement" from
*The Socratic Method: A Practitioner's Handbook* (Godine, 2021), condensed in
`references/rules-of-engagement.md`.
