Base directory for this skill: /Users/tjb/.claude/skills/todoist-sync

# Todoist Sync Skill

## Purpose

Extract TODO items from markdown planning documents and sync them to Todoist. This skill handles complex parsing, validation, and batch processing with state tracking to support updates.

## When to Activate

This skill activates when:
- User runs `/todo-sync [path]`
- User asks to "sync TODOs to Todoist"
- User wants to "extract tasks from markdown files"
- User mentions "add all TODOs to Todoist"

## Workflow

### 1. Discover Files

If given a directory:
- Use Glob to find all `*.md` and `*.qmd` files
- Exclude files in `.git/`, `node_modules/`, etc.
- Sort by modification time (most recent first)

If given a specific file:
- Verify it exists with Read
- Process only that file

### 2. Parse TODO Items

For each markdown file, extract items matching these patterns:

#### Hard Deadlines (Priority 1)
- `DUE: YYYY-MM-DD` or `Deadline: YYYY-MM-DD`
- `Due: Month DD, YYYY` (e.g., "Due: November 15, 2025")
- Add P1 (urgent) priority for explicit deadlines

#### TODO Items (Priority 4)
- `- [ ] TODO: Task description`
- Explicit TODO markers in checkbox format

#### Milestones with Dates (Priority 4)
- `- [ ] Task name (by YYYY-MM-DD)`
- `- [ ] Task name (YYYY-MM-DD)`
- Tasks with target dates in parentheses

#### Generic Checkbox Tasks (Priority 4)
- `- [ ] Task description`
- Only if not matched by more specific patterns

#### Questions/Issues (Priority 4)
- `Question: Description`
- `Open Issue: Description`
- Tagged with additional "question" label

### 3. Use Parsing Script

Delegate extraction to `scripts/parse-todos.py`:

```bash
python3 ~/.claude/skills/todoist-sync/scripts/parse-todos.py [markdown-file]
```

The script outputs JSON:
```json
[
  {
    "type": "deadline",
    "content": "Submit manuscript",
    "due_date": "2025-12-15",
    "due_string": "2025-12-15 17:00",
    "priority": 1,
    "labels": ["evaluation-game"],
    "source_file": "plans/evaluation_game_plan.qmd",
    "source_line": 23
  },
  ...
]
```

### 4. Validate Items

For each extracted item:
- Verify content is not empty
- Check for valid date formats
- Warn about past dates (but allow if user confirms)
- Ensure required fields present (content, labels)

### 5. Confirm with User

**IMPORTANT**: Always show extracted items and ask for confirmation before syncing.

Present in a table:
```
Found 12 TODO items:

Type       | Content                       | Due Date   | Priority | Labels
-----------|-------------------------------|------------|----------|------------------
Deadline   | Submit manuscript             | 2025-12-15 | P1       | evaluation-game
TODO       | Add abstract                  | —          | P4       | evaluation-game
Milestone  | Complete MCMC implementation  | 2025-11-22 | P4       | evaluation-game
Task       | Identify necessary packages   | —          | P4       | scored-bayesian
Question   | What is target application?   | —          | P4       | syndicated-monte

Proceed with syncing these tasks to Todoist? (yes/no)
```

### 6. Sync to Todoist

For each confirmed item:

1. Generate task data:
   - Content from the TODO item
   - Due date (if present)
   - Priority (1 for deadlines, 4 for others)
   - Labels based on source file
   - Description with source location

2. Check sync state:
   - Load `.todoist-sync-state.json` to find existing task IDs
   - If task exists, update it
   - If task doesn't exist or was deleted, create new one

3. Execute sync via `scripts/sync-todoist.py`:
   ```bash
   python3 ~/.claude/skills/todoist-sync/scripts/sync-todoist.py [todos.json]
   ```

4. Track results:
   - Created tasks
   - Updated tasks
   - Skipped tasks
   - Errors

### 7. Report Results

After completion:
```
Todoist Sync Complete

Files scanned: 3
TODO items found: 12
Tasks created: 8
Tasks updated: 4
Errors: 0

Details:
✓ Created: Submit manuscript (2025-12-15) [evaluation-game]
✓ Created: Add abstract [evaluation-game]
✓ Updated: Complete MCMC implementation (2025-11-22) [evaluation-game]
✓ Created: Identify necessary packages [scored-bayesian]
...
```

## Error Handling

### Past Dates
If date is in the past:
- Include in preview with warning indicator
- User can choose to sync anyway during confirmation

### Invalid Dates
If date can't be parsed:
- Log warning: "Could not parse date in [file]:[line]: [text]"
- Create task without due date
- Continue processing

### No Items Found
If no TODO items found:
- Report: "No TODO items found in [files]"
- Suggest adding TODOs using the documented formats
- Exit gracefully

### Todoist API Errors
If API request fails:
- Display error message with HTTP status
- Continue with remaining tasks if possible
- Report errors in final summary

### Missing API Token
If `TODOIST_API_TOKEN` not configured:
- Provide clear error message
- Direct user to README for setup instructions
- Exit with helpful guidance

## Date Handling

### Supported Formats

**ISO Format** (preferred):
- `2025-11-15`
- `2025-11-15 14:30`

**Written Format**:
- `November 15, 2025`
- `Nov 15, 2025`
- `15 November 2025`

**Due String** (passed to Todoist):
- Todoist will parse natural language dates
- "tomorrow", "next Friday", etc.

### Default Times

If time not specified:
- Deadlines → 5pm (17:00)
- Milestones → 9am (09:00)
- Other tasks → no time (all-day)

## Label Strategy

Labels are automatically generated from source file names:

- `plans/evaluation_game_plan.qmd` → `evaluation-game`
- `plans/scored_bayesian_computation_plan.qmd` → `scored-bayesian`
- `notes/research_notes.md` → `research-notes`

Additional labels:
- `question` for question/issue items

## Priority Mapping

| Source Pattern | Todoist Priority | Description |
|----------------|------------------|-------------|
| `DUE:` / `Deadline:` | P1 (urgent) | Explicit deadlines |
| All other items | P4 (normal) | Regular tasks |

Todoist priorities:
- P1 = 4 (urgent, red)
- P2 = 3 (high, orange)
- P3 = 2 (medium, yellow)
- P4 = 1 (normal, no color)

## State Tracking

Sync state is stored in `.todoist-sync-state.json` at the project root:

```json
{
  "tasks": {
    "abc123hash": "1234567890",
    "def456hash": "9876543210"
  }
}
```

Each TODO is hashed based on:
- Source file path
- Line number
- Content

This allows the system to:
- Detect when TODO content changes and update the Todoist task
- Avoid creating duplicate tasks on re-run
- Maintain sync between markdown and Todoist

**IMPORTANT**: Add `.todoist-sync-state.json` to `.gitignore`

## Dry Run Mode

Support `--dry-run` flag for testing:
- Parse and validate all TODOs
- Show what would be created/updated
- Don't actually sync to Todoist
- Don't modify state file

## Tips for Users

Recommend these formats in planning documents:

```markdown
## Timeline

- **DUE: 2025-12-15 17:00** — Submit final manuscript
- [ ] TODO: Add abstract
- [ ] Complete MCMC implementation (by 2025-11-22)

## Open Questions

- **Question:** What is the target application domain?
- **Open Issue:** Need to clarify scoring rule definition

## Tasks

- [ ] Define "scored" approach formally
- [ ] Establish theoretical properties
- [ ] Implement basic algorithm
```

## Configuration

### API Token Setup

1. Get token from Todoist:
   - Settings → Integrations → Developer tab
   - Copy API token

2. Store in `.env` file:
   ```bash
   echo "TODOIST_API_TOKEN=your_token_here" > ~/.claude/skills/todoist-sync/.env
   ```

3. Or set as environment variable:
   ```bash
   export TODOIST_API_TOKEN=your_token_here
   ```

### Gitignore Recommendations

Add to `.gitignore`:
```
.todoist-sync-state.json
.env
```

## Performance Notes

- For large directories (>50 files), only scan files modified in last 90 days
- Process files sequentially (API rate limits)
- Cache parsed results for 5 minutes
- Batch operations not supported by Todoist API v1 (must create tasks one by one)

## Integration with Other Tools

This skill can be extended to work with:
- Git hooks (auto-sync on commit)
- File watchers (auto-sync when planning docs change)
- Other task management tools with adapter scripts
