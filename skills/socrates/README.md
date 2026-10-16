# socrates

A Socratic dialogue on any reading. Claude plays Socrates and questions you on
an article, book chapter, white paper, or blog post until you can state what it
says, and what you think of it, in your own words. It ends when you give a three
to five sentence summary that Socrates accepts, and the summary plus transcript
are saved beside the source.

Socrates never summarizes the reading, never answers a content question, and
never moves on until you have captured the current point. The conduct rules are
Ward Farnsworth's twelve "Socratic Rules of Engagement" from *The Socratic
Method: A Practitioner's Handbook* (2021).

## Use

```
/socrates "path/to/paper.pdf"
/socrates "path/to/chapter.md" --sections 2-4
/socrates https://example.org/some-essay
/socrates "The Problem of Social Cost" by Coase
/socrates "paper.pdf" --gentle
/socrates "paper.pdf" --no-notes
```

Or just ask: *"question me on this reading"*, *"play Socrates on chapter 3"*.

Flags, all optional:

| Flag | Effect |
|---|---|
| `--pages A-B`, `--sections A-B` | Confine the dialogue to part of a long source. |
| `--gentle` | Fewer refutations, more scaffolding. Default is firm. |
| `--no-notes` | Skip the notes file at the end. |

Say them in words if you prefer: "go easy on me", "just the first half".

## How a session goes

1. Socrates reads the whole reading, silently.
2. Socrates states the rules in a few lines and asks one broad question about
   what the author is trying to do.
3. You answer in your own words, citing pages. Socrates asks one question at
   a time. When you are right, you move on. When you are wrong, Socrates finds
   something you both agree on and asks how it squares with what you said.
   When you are stuck, Socrates sends you to a page.
4. When every load-bearing part of the reading is covered, Socrates asks for
   your three to five sentence summary. It has to be your words, it has to get
   the reading right, and it has to contain a judgment with a reason.
5. Socrates accepts it, says so, and stops.
6. The summary, the lines of questioning, and the transcript are written to
   `Socratic Dialogue -- <Title>.md` next to the source.

A thorough session is ten to twenty exchanges.

You can say **"I'm stuck"** to get a narrower question and **"point me to the
text"** to get a page to reread. You cannot get Socrates to explain the reading
to you. That is the point.

## Install

### Claude Code

Copy or clone this folder to `~/.claude/skills/socrates`:

```sh
mkdir -p ~/.claude/skills
cp -r socrates ~/.claude/skills/socrates
```

Then in any Claude Code session, `/socrates <reference>`.

If you keep skills in a repo, symlink instead so edits take effect at once:

```sh
ln -sfn "$PWD/socrates" ~/.claude/skills/socrates
```

### claude.ai without Claude Code

See `prompts/claude-ai-prompt.md`. Attach the reading and the Rules of
Engagement PDF to a new chat and paste the prompt there.

## What's in the box

| Path | |
|---|---|
| `SKILL.md` | The persona, the dialogue loop, the exit criteria |
| `references/rules-of-engagement.md` | Farnsworth's twelve rules, condensed, with what each means in a dialogue |
| `references/Socratic Rules of Engagement.pdf` | The epilogue itself |
| `references/question-bank.md` | Questions by situation, for when the right one does not come |
| `templates/session-notes.md` | The notes skeleton |
| `prompts/claude-ai-prompt.md` | The exercise as a copy-paste prompt for the web app |

## Design notes

The exercise was first run as a one-paragraph prompt with two attachments. The
skill keeps that shape and adds the things a prompt could not enforce: Socrates
reads the whole text first and builds a private checklist of load-bearing
moves, so "move on only when the student has it" has something concrete behind
it; the elenchus is the default response to a wrong answer rather than a
correction; and the accepted summary has to contain the student's own
judgment, not just a restatement.

The Liberty Fund seminar procedures that accompanied the original material are
written for a room with hand signals and a queue. Four of their norms transfer
to a dialogue and are in the rules file: no lecturing, text-based, the leader
facilitates rather than teaches, cite the page. The rest are left out.

Pairs with the `reading-guide` skill, which does the opposite job: it tells
you what the text says. Use that one when you want a summary. Use this one
when you want to find out whether you have one.
