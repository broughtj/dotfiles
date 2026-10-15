---
name: calendar-sync
description: Parse markdown files for deadlines, milestones, meetings, and conferences; batch-add to Fantastical. Activate when user wants to sync calendar items from planning documents.
allowed-tools: Read, Bash, Grep, Glob
---

# Calendar Sync Skill

## Purpose

Extract calendar-worthy items from markdown planning documents and batch-create Fantastical events. This skill handles complex parsing, validation, and batch processing.

## When to Activate

This skill activates when:
- User runs `/cal-sync [path]`
- User asks to "sync calendar from planning docs"
- User wants to "extract deadlines from markdown files"
- User mentions "add all dates to Fantastical"

## Workflow

### 1. Discover Files

If given a directory:
- Use Glob to find all `*.md` files
- Exclude files in `.git/`, `node_modules/`, etc.
- Sort by modification time (most recent first)

If given a specific file:
- Verify it exists with Read
- Process only that file

### 2. Parse Calendar Items

For each markdown file, extract items matching these patterns:

#### Hard Deadlines
- `DUE: YYYY-MM-DD` or `Deadline: YYYY-MM-DD`
- `Due: Month DD, YYYY` (e.g., "Due: November 15, 2025")
- `Submit by [date]` or `Complete by [date]`
- Add "alert 1 week before" for deadlines

#### Soft Milestones
- `- [ ] Task name (by YYYY-MM-DD)`
- `- [ ] Task name (YYYY-MM-DD)`
- Milestone markers in task lists
- Add "alert 1 day before" for milestones

#### Recurring Meetings
- `Meeting: [description] [day] at [time]` (e.g., "Meeting: Advisor check-in Thursday at 2pm")
- `Weekly [description]: [day] [time]`
- Look for "recurring", "weekly", "biweekly"
- Extract recurrence pattern

#### Conference Dates
- `Conference: [name] [start date]-[end date]`
- `[Conference name]: [Month DD-DD, YYYY]`
- Multi-day events with location
- Add "alert 1 month before" for conferences

### 3. Use Parsing Script

Delegate complex extraction to `scripts/parse-dates.py`:

```bash
python3 ~/.claude/skills/calendar-sync/scripts/parse-dates.py [markdown-file]
```

The script outputs JSON:
```json
[
  {
    "type": "deadline",
    "title": "Submit manuscript",
    "date": "2025-12-15",
    "time": "17:00",
    "alert": "1 week before",
    "source_file": "project-plan.md",
    "source_line": 23
  },
  ...
]
```

### 4. Validate Items

For each extracted item:
- Verify date is valid (exists, not in far past)
- Check for duplicates (same title + date)
- Warn about past dates (but allow if user confirms)
- Ensure required fields present (title, date)

### 5. Confirm with User

**IMPORTANT**: Always show extracted items and ask for confirmation before creating.

Present in a table:
```
Found 5 calendar items:

Type       | Title                    | Date       | Time  | Alert
-----------|--------------------------|------------|-------|---------------
Deadline   | Submit manuscript        | 2025-12-15 | 17:00 | 1 week before
Milestone  | Complete MCMC analysis   | 2025-11-22 | 09:00 | 1 day before
Meeting    | Advisor check-in         | Weekly Thu | 14:00 | 30 min before
Conference | JSM 2025                 | 2025-08-02 | —     | 1 month before
Milestone  | Draft results section    | 2025-11-30 | 09:00 | 1 day before

Proceed with creating these events in Fantastical? (yes/no)
```

### 6. Batch Create Events

For each confirmed item:

1. Generate Fantastical natural language sentence:
   ```
   Deadline: "Submit manuscript December 15, 2025 at 5pm alert 1 week before"
   Meeting: "Advisor check-in every Thursday at 2pm starting this week"
   Conference: "JSM 2025 August 2-7 2025 in Seattle alert 1 month before"
   ```

2. URL-encode the sentence

3. Generate command:
   ```bash
   open "x-fantastical3://parse?sentence=[encoded-sentence]"
   ```

4. Execute each command with small delay (0.5s between events to avoid overwhelming)

### 7. Report Results

After completion:
```
Calendar Sync Complete

Files scanned: 3
Items found: 5
Events created: 5
Items skipped: 0

Details:
✓ Submit manuscript (2025-12-15)
✓ Complete MCMC analysis (2025-11-22)
✓ Advisor check-in (recurring Thursday 2pm)
✓ JSM 2025 (2025-08-02 to 2025-08-07)
✓ Draft results section (2025-11-30)
```

## Error Handling

### Past Dates
If date is in the past:
- Warn user: "Note: [title] is scheduled for [past date]"
- Ask: "Include anyway? (yes/no)"
- Skip if user declines

### Invalid Dates
If date can't be parsed:
- Log warning: "Could not parse date in [file]:[line]: [text]"
- Skip item
- Continue processing

### No Items Found
If no calendar items found:
- Report: "No calendar items found in [files]"
- Suggest using the template: `templates/planning-doc-template.md`
- Exit gracefully

### Fantastical Not Installed
If `open "x-fantastical3://..."` fails:
- Check if Fantastical is installed
- Provide installation link: https://flexibits.com/fantastical
- Exit with helpful error message

## Date Parsing Rules

### Supported Formats

**ISO Format** (preferred):
- `2025-11-15`
- `2025-11-15 14:30`

**Written Format**:
- `November 15, 2025`
- `Nov 15, 2025`
- `15 November 2025`

**Relative** (let Fantastical handle):
- "next Friday"
- "in 2 weeks"
- "tomorrow at 2pm"

**Time Formats**:
- `14:30` or `2:30pm` or `2pm`
- Default to 9am for deadlines without time
- Default to 5pm for submission deadlines

### Ambiguous Cases

If time not specified:
- Deadlines → 5pm (end of business day)
- Milestones → 9am (start of work day)
- Meetings → require explicit time (error if missing)
- Conferences → all-day events

## Tips for Users

Recommend this format in planning documents (use template):

```markdown
## Timeline

- **DUE: 2025-12-15 17:00** — Submit final manuscript
- **Milestone: 2025-11-22** — Complete MCMC implementation

## Meetings

- **Weekly: Thursday 14:00** — Advisor check-in
- **Meeting: 2025-11-08 10:00** — Collaborator call (zoom)

## Conferences

- **Conference: JSM 2025 (2025-08-02 to 2025-08-07)** — Seattle, WA
```

## Supporting Files

- **scripts/parse-dates.py**: Python script for complex regex extraction
- **templates/planning-doc-template.md**: Recommended format for planning docs
- **examples/sample-project.md**: Example project with properly formatted dates

## Performance Notes

- For large directories (>50 files), only scan files modified in last 90 days
- Process files in parallel if >10 files (but create events sequentially)
- Cache parsed results to avoid re-parsing if re-run immediately

## Integration with Other Tools

This skill can be extended to work with:
- Git hooks (auto-sync on commit)
- File watchers (auto-sync when planning docs change)
- Other calendar tools (Google Calendar, iCal) with adapter scripts
