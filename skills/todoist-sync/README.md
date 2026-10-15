# Todoist Sync Skill

Automatically extract TODO items from your markdown planning documents and sync them to Todoist.

## Quick Start

### 1. Get Your Todoist API Token

1. Open [Todoist](https://todoist.com) and log in
2. Go to Settings → Integrations
3. Click the "Developer" tab
4. Copy your API token

### 2. Configure the Skill

Create a `.env` file with your API token:

```bash
echo "TODOIST_API_TOKEN=your_token_here" > ~/.claude/skills/todoist-sync/.env
```

### 3. Use the Slash Command

Sync TODOs from your current directory:

```
/todo-sync
```

Or sync a specific file or directory:

```
/todo-sync plans/evaluation_game_plan.qmd
/todo-sync plans/
```

## What Gets Synced?

The skill recognizes these patterns in your markdown files:

### Deadlines (Priority 1 - Urgent)

```markdown
- **DUE: 2025-12-15 17:00** — Submit final manuscript
- **Deadline: November 15, 2025** — Complete revisions
```

### TODO Items (Priority 4 - Normal)

```markdown
- [ ] TODO: Add abstract
- [ ] TODO: Review literature section
```

### Milestones with Dates (Priority 4 - Normal)

```markdown
- [ ] Complete MCMC implementation (by 2025-11-22)
- [ ] Draft results section (2025-11-30)
```

### Generic Tasks (Priority 4 - Normal)

```markdown
- [ ] Identify necessary Julia packages
- [ ] Set up computational environment
```

### Questions/Issues (Priority 4 - Normal)

```markdown
- **Question:** What is the target application domain?
- **Open Issue:** Need to clarify scoring rule definition
```

## Features

### Smart Organization

- **Labels**: Tasks are automatically labeled based on their source file
  - `plans/evaluation_game_plan.qmd` → `@evaluation-game`
  - `plans/scored_bayesian_computation_plan.qmd` → `@scored-bayesian`

- **Priorities**:
  - Explicit deadlines (DUE:, Deadline:) → P1 (urgent)
  - Everything else → P4 (normal)

### State Tracking

The skill tracks which tasks have been synced using `.todoist-sync-state.json`:

- **No duplicates**: Re-running the sync won't create duplicate tasks
- **Updates**: If you change a TODO in your markdown, the Todoist task will be updated
- **Deletions**: If you delete a TODO from markdown, the Todoist task remains (manual cleanup)

### Source Tracking

Each Todoist task includes a description with the source location:

```
Source: plans/evaluation_game_plan.qmd:156
```

This makes it easy to find the original context for any task.

## Example Workflow

1. **Write your planning document** with TODOs:

```markdown
## Timeline

- **DUE: 2025-12-15 17:00** — Submit final manuscript
- [ ] TODO: Add abstract (150-250 words)
- [ ] Complete MCMC implementation (by 2025-11-22)

## Open Questions

- **Question:** What is the best prior for the variance parameter?
```

2. **Run the sync**:

```
/todo-sync plans/my_project.qmd
```

3. **Review the preview**:

```
Found 4 TODO items:

Type       | Content                       | Due Date   | Priority | Labels
-----------|-------------------------------|------------|----------|------------
Deadline   | Submit final manuscript       | 2025-12-15 | P1       | my-project
TODO       | Add abstract (150-250 words)  | —          | P4       | my-project
Milestone  | Complete MCMC implementation  | 2025-11-22 | P4       | my-project
Question   | Best prior for variance?      | —          | P4       | my-project

Proceed with syncing these tasks to Todoist? (yes/no)
```

4. **Confirm and sync**

5. **See results in Todoist**:
   - All 4 tasks appear in your Inbox
   - Each labeled with `@my-project`
   - Deadline task is marked urgent (P1)
   - Question task has additional `@question` label

## Dry Run Mode

Test the sync without actually creating tasks:

```bash
python3 ~/.claude/skills/todoist-sync/scripts/parse-todos.py plans/my_project.qmd > todos.json
python3 ~/.claude/skills/todoist-sync/scripts/sync-todoist.py todos.json --dry-run
```

## Configuration

### Environment Variable

Instead of using `.env`, you can set the token as an environment variable:

```bash
export TODOIST_API_TOKEN=your_token_here
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

### Gitignore

Add these to your project's `.gitignore`:

```
.todoist-sync-state.json
.env
```

## Troubleshooting

### "TODOIST_API_TOKEN not found"

Make sure you've created the `.env` file with your API token:

```bash
cat ~/.claude/skills/todoist-sync/.env
```

Should show:
```
TODOIST_API_TOKEN=your_actual_token_here
```

### "No TODO items found"

The skill looks for specific patterns. Make sure your TODOs use one of the supported formats:

- `- [ ] TODO: Description`
- `- [ ] Task name (by YYYY-MM-DD)`
- `- **DUE: YYYY-MM-DD** — Description`

### Duplicate Tasks

If you're getting duplicate tasks, make sure the `.todoist-sync-state.json` file exists and isn't being deleted between runs.

### API Rate Limits

Todoist has rate limits on API requests. If you're syncing many tasks:

- The script processes tasks sequentially
- Wait a few seconds between large syncs
- Consider syncing one file at a time

## Advanced Usage

### Sync Multiple Files

```
/todo-sync plans/
```

This will scan all `.md` and `.qmd` files in the `plans/` directory.

### Update Existing Tasks

Just edit your markdown file and re-run the sync:

1. Change TODO content in markdown
2. Run `/todo-sync` again
3. The existing Todoist task will be updated (not duplicated)

### Manual Sync with Scripts

For automation or custom workflows:

```bash
# Parse TODOs from a file
python3 ~/.claude/skills/todoist-sync/scripts/parse-todos.py input.md > todos.json

# Sync to Todoist
python3 ~/.claude/skills/todoist-sync/scripts/sync-todoist.py todos.json
```

## Privacy & Security

- Your API token is stored locally in `~/.claude/skills/todoist-sync/.env`
- Never commit `.env` to git
- The sync state file (`.todoist-sync-state.json`) only contains task IDs and hashes, no sensitive data
- All communication with Todoist uses HTTPS

## Support

For issues or questions:
- Check the [Todoist API documentation](https://developer.todoist.com/rest/v2/)
- Review the skill source code in `~/.claude/skills/todoist-sync/`
- Ask Claude Code for help with specific error messages

## Tips

1. **Use consistent date formats**: ISO format (`YYYY-MM-DD`) is most reliable
2. **Label your deadlines clearly**: Use `DUE:` or `Deadline:` for important dates
3. **Keep TODOs concise**: Short, actionable tasks work best
4. **Review before syncing**: Always check the preview before confirming
5. **Sync regularly**: Run `/todo-sync` after updating your planning documents

## What's Not Synced

These items are intentionally not synced:

- Completed checkboxes (`[x]`)
- Comments in code blocks
- TODOs in frontmatter
- Section headings (even if they contain "TODO")

## Related Tools

- **Calendar Sync** (`/cal-sync`): Sync deadlines and meetings to Fantastical
- **Git Commits**: Track your progress with descriptive commits
- **Quarto**: Render your planning documents to beautiful PDFs
