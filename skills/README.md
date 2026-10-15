# Agent skills

Portable [Agent Skills](https://agentskills.io) used with Claude Code. Each
subdirectory is one skill: a `SKILL.md` with frontmatter plus any `scripts/`,
`assets/`, `references/`, or `templates/` it needs.

## Install

Claude Code reads user-level skills from `~/.claude/skills`. Symlink each skill
there so edits in the repo take effect immediately:

```sh
mkdir -p ~/.claude/skills
for s in skills/*/; do
  s=${s%/}
  ln -sfn "$PWD/$s" ~/.claude/skills/"$(basename "$s")"
done
```

`todoist-sync` needs a Todoist API token. Copy its `.env.template` to `.env`
beside the scripts and fill it in; `.env` files are git-ignored.

## Skills

| Skill | Purpose |
|---|---|
| `calendar-sync` | Parse markdown planning docs for deadlines, meetings, and conferences and batch-add them to Fantastical. |
| `reading-guide` | Produce a CliffsNotes-style reading guide to a paper or chapter, delivered as Markdown, a published Artifact, and a Quarto document. |
| `slides` | Build a lecture deck (Metropolis Beamer PDF, revealjs HTML, Typst handout) in the course theme via the `usu-slides` Quarto extension. |
| `todoist-sync` | Scan markdown files for TODO items and sync them to Todoist. |
