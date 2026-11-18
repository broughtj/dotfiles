# tmux

Config lives at `~/.config/tmux/tmux.conf`. This directory holds a tracked copy,
a one-page cheatsheet, and a `justfile` that drives both.

| File             | What it is                                          |
| ---------------- | --------------------------------------------------- |
| `tmux.conf`      | tracked copy of the config                          |
| `cheatsheet.qmd` | cheatsheet source (Quarto, compiled with Typst)     |
| `cheatsheet.pdf` | the rendered cheatsheet, one landscape page         |
| `justfile`       | recipes for building the cheatsheet and syncing the config |

## Install

```sh
just install    # copy tmux.conf into ~/.config/tmux/ and reload tmux
```

This overwrites the live config. Run `just diff` first to see what would change.
Without [just](https://github.com/casey/just):

```sh
mkdir -p ~/.config/tmux
cp tmux.conf ~/.config/tmux/tmux.conf
```

Requires a Nerd Font for the status bar glyphs (the Ghostty config in this
repo already sets one). Colors are Catppuccin Mocha.

## Justfile

Run `just` in this directory to list the recipes.

| Recipe         | Action                                                    |
| -------------- | --------------------------------------------------------- |
| `just render`  | compile the cheatsheet to PDF                             |
| `just open`    | compile, then open the PDF                                |
| `just watch`   | recompile on every save, with a live preview              |
| `just clean`   | remove build byproducts (keeps the PDF)                   |
| `just diff`    | diff the tracked config against the live one              |
| `just install` | copy the tracked config into place and reload tmux        |
| `just pull`    | copy the live config back into the repo                   |
| `just reload`  | re-source the live config in the running tmux server      |

## Cheatsheet

`cheatsheet.pdf` is a printable summary of the key bindings below. A gold dot
marks bindings defined in `tmux.conf`; unmarked rows are tmux defaults.

Building it needs [Quarto](https://quarto.org) (which bundles Typst) and the
Fira Sans and Fira Mono fonts. The layout is written directly in Typst inside
`cheatsheet.qmd`, and each binding is one `(custom?, keys, action)` row, so
adding a binding to the config means adding one line there and running
`just render`.

## Workflow

Prefix is `C-a` (not the default `C-b`). Below, `P` means "press the prefix first".

### Sessions

One session per project. Name it after the project and detach instead of
quitting, so the shells, REPLs, and popups survive between terminal windows.

```sh
tmux new -s proj          # start a named session
tmux ls                   # list sessions
tmux attach -t proj       # reattach (or: tmux a -t proj)
tmux kill-session -t proj # tear one down
```

| Keys    | Action                              |
| ------- | ----------------------------------- |
| `P d`   | detach, leave the session running   |
| `P s`   | pick a session from a list          |
| `P (` / `P )` | previous / next session       |
| `P $`   | rename the current session          |

### Windows

Windows are numbered from 1. New windows open in the current pane's directory.

| Keys           | Action                          |
| -------------- | ------------------------------- |
| `P c`          | new window                      |
| `P n` / `P p`  | next / previous window          |
| `P 1`..`P 9`   | jump to window by number        |
| `P ,`          | rename window                   |
| `P w`          | pick a window from a list       |
| `C-S-Left/Right` | move the current window left / right (no prefix) |
| `F1`           | renumber windows to close gaps (no prefix) |
| `P &`          | kill window                     |

### Panes

Splits also open in the current pane's directory. Mouse is on, so you can
click to focus a pane and drag borders to resize.

| Keys          | Action                      |
| ------------- | --------------------------- |
| `P %`         | split left / right          |
| `P "`         | split top / bottom          |
| `P` + arrows  | move between panes          |
| `P z`         | zoom / unzoom a pane        |
| `P x`         | kill pane                   |

### Popups

Popups are floating scratch windows that close when the command exits.
Use them for a quick REPL or shell without disturbing the pane layout.

| Keys    | Opens                                       |
| ------- | ------------------------------------------- |
| `P C-t` | zsh in the current directory (90%)          |
| `P C-j` | `julia --project=.` (90%)                   |
| `P C-p` | `ipython`                                   |
| `P C-z` | `nvim ~/.zshrc` (85%)                       |

### Copy mode and scrollback

History is 100k lines. `P [` enters copy mode, `q` leaves it. Scrolling
with the mouse also enters copy mode.

### Reload

After editing the config, `P r` reloads it in place. Copy the file back here
and commit when it settles.

```sh
just pull
```

If the change adds or moves a binding, update `cheatsheet.qmd` and run
`just render` as well.

## Notes on settings

- `escape-time 0` so Esc in Neovim is instant.
- `focus-events` and `extended-keys` (csi-u) on, so Neovim and modern CLIs
  see focus changes and modifier combos.
- Terminal title follows the active pane's title.
