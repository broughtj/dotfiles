# Agent skills

Portable [Agent Skills](https://agentskills.io) used with Claude Code. Each
subdirectory is one skill: a `SKILL.md` with frontmatter plus any `scripts/`,
`assets/`, and `reference/` it needs.

## Install

Symlink a skill into Claude Code's user-level skills directory:

```sh
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/slides" ~/.claude/skills/slides
```

## Skills

| Skill | Purpose |
|---|---|
| `slides` | Build a lecture deck (Metropolis Beamer PDF, revealjs HTML, Typst handout) in the course theme via the `usu-slides` Quarto extension. |
