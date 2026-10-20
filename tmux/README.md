# tmux

Config lives at `~/.config/tmux/tmux.conf`. This directory holds a tracked copy.

## Install

```sh
mkdir -p ~/.config/tmux
cp tmux/tmux.conf ~/.config/tmux/tmux.conf
```

Requires a Nerd Font for the status bar glyphs (the Ghostty config in this
repo already sets one). Colors are Catppuccin Mocha.

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
cp ~/.config/tmux/tmux.conf tmux/tmux.conf
```

## Notes on settings

- `escape-time 0` so Esc in Neovim is instant.
- `focus-events` and `extended-keys` (csi-u) on, so Neovim and modern CLIs
  see focus changes and modifier combos.
- Terminal title follows the active pane's title.
