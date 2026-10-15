# Fantastical Calendar Sync

A hybrid system for managing your calendar from planning documents using Claude Code and Fantastical.

## Overview

This system provides two approaches to calendar management:

1. **Quick Add** (`/cal-add`): Manually create single events using natural language
2. **Batch Sync** (`/cal-sync`): Automatically extract and create multiple events from planning documents

## Installation

All files are already installed in `~/.claude/`:

```
~/.claude/
├── commands/
│   ├── cal-add.md          # Quick add command
│   └── cal-sync.md         # Batch sync command
└── skills/
    └── calendar-sync/
        ├── SKILL.md                         # Main skill instructions
        ├── scripts/
        │   └── parse-dates.py              # Date extraction script
        ├── templates/
        │   └── planning-doc-template.md    # Recommended format
        └── examples/
            └── sample-project.md           # Example with 35 items
```

## Quick Start

### Method 1: Quick Add Single Event

Use `/cal-add` for one-off events:

```
/cal-add Submit paper December 15 at 5pm, alert 1 week before
```

Claude will:
1. Parse your natural language input
2. Generate a Fantastical URL
3. Open Fantastical to create the event

### Method 2: Batch Sync from Files

Use `/cal-sync` to extract all calendar items from planning documents:

```
/cal-sync path/to/project-plan.md
```

Or sync an entire directory:

```
/cal-sync path/to/project/
```

Claude will:
1. Find and read markdown files
2. Extract calendar items (deadlines, milestones, meetings, conferences)
3. Show you a summary table
4. Ask for confirmation
5. Create all events in Fantastical
6. Report results

## Supported Calendar Item Types

### 1. Hard Deadlines

**Format:**
```markdown
**DUE: 2025-12-15 17:00** — Submit final manuscript
**Deadline: November 22, 2025** — IRB application
**Complete by: December 1, 2025** — Finish data collection
```

**Auto-generated:**
- Default time: 5pm (if not specified)
- Alert: 1 week before

### 2. Soft Milestones

**Format:**
```markdown
- [ ] Complete literature review (by 2025-11-15)
- [ ] Finish MCMC implementation (2025-11-22)
- [ ] Draft results section (by 2025-11-30)
```

**Auto-generated:**
- Default time: 9am
- Alert: 1 day before

### 3. Recurring Meetings

**Format:**
```markdown
**Weekly: Thursday 14:00** — Advisor check-in (Zoom)
**Recurring Meeting: Tuesday 10:00** — Lab meeting (Room B)
```

**Auto-generated:**
- Recurrence: Weekly
- Alert: 30 minutes before

### 4. One-Time Meetings

**Format:**
```markdown
**Meeting: Biostatistician consult 2025-11-10 at 10:00**
**Call: Collaborator discussion 2025-11-15 at 2pm** — Zoom
```

**Auto-generated:**
- Alert: 30 minutes before

### 5. Conferences & Multi-Day Events

**Format:**
```markdown
**Conference: JSM 2025 (2025-08-02 to 2025-08-07)** — Seattle, WA
**Event: BayesComp 2026 (2026-03-15 to 2026-03-20)** — Valencia
```

**Auto-generated:**
- All-day event
- Alert: 1 month before

## Date Format Support

### ISO Format (Recommended)
```
2025-11-15
2025-11-15 14:30
```

### Written Format
```
November 15, 2025
Nov 15, 2025 at 2pm
15 November 2025
```

### Time Formats
```
14:30
2:30pm
2pm
```

## Example Workflow

### 1. Create a Planning Document

Use the template as a guide:

```bash
cp ~/.claude/skills/calendar-sync/templates/planning-doc-template.md ~/my-project/plan.md
```

Edit with your deadlines, milestones, meetings, and conferences.

### 2. Sync to Fantastical

```
/cal-sync ~/my-project/plan.md
```

### 3. Review Before Creating

Claude will show you a summary:

```
Found 15 calendar items:

Type       | Title                    | Date       | Time  | Alert
-----------|--------------------------|------------|-------|---------------
Deadline   | Submit manuscript        | 2025-12-15 | 17:00 | 1 week before
Milestone  | Complete MCMC analysis   | 2025-11-22 | 09:00 | 1 day before
Meeting    | Advisor check-in         | Thursday   | 14:00 | 30 min before
Conference | JSM 2025                 | 2025-08-02 | —     | 1 month before
...

Proceed with creating these events in Fantastical? (yes/no)
```

### 4. Confirm and Create

Type `yes` and Claude will create all events.

## Tips & Best Practices

### For Deadlines
- Use ISO format (YYYY-MM-DD) to avoid ambiguity
- Include specific times for submission deadlines
- Add context in titles: "Submit NSF grant" not just "Submit"

### For Milestones
- Keep checkbox format for easy tracking
- Be specific: "Draft methods section" not "Write"
- Use realistic dates

### For Meetings
- Always include times for meetings
- Add location (Zoom, room number, etc.) in title
- Use recurring format for regular meetings

### For Conferences
- Include location in title or after em-dash
- Add abstract/registration deadlines as separate items
- Use date range format for multi-day events

## Testing

Test the parser directly without creating events:

```bash
python3 ~/.claude/skills/calendar-sync/scripts/parse-dates.py path/to/plan.md
```

This outputs JSON showing all extracted items.

Test with the example file:

```bash
python3 ~/.claude/skills/calendar-sync/scripts/parse-dates.py \
  ~/.claude/skills/calendar-sync/examples/sample-project.md
```

Expected output: 35 items (10 deadlines, 15 milestones, 8 meetings, 2 conferences)

## Troubleshooting

### No items found?
- Check that dates are in supported formats
- Ensure keywords are present (DUE, Meeting, Conference, Weekly)
- Verify file is valid markdown
- Try the template format

### Wrong dates parsed?
- Use ISO format (YYYY-MM-DD) for clarity
- Include year in all dates
- Be explicit with times (14:00 vs "2pm")

### Events not creating?
- Ensure Fantastical is installed and running
- Check URL scheme permissions in macOS System Settings
- Try creating one event manually first with `/cal-add Test event tomorrow at 2pm`

### Parser errors?
- Check Python 3 is installed: `python3 --version`
- Verify script is executable: `ls -l ~/.claude/skills/calendar-sync/scripts/parse-dates.py`
- Test on example file first to isolate issue

## Extending the System

### Adding New Date Patterns

Edit `scripts/parse-dates.py` and add new regex patterns to the `PATTERNS` dictionary.

### Customizing Alerts

Modify the `alert` parameter in `SKILL.md` or `parse-dates.py`:
- Deadlines: Currently "1 week before"
- Milestones: Currently "1 day before"
- Meetings: Currently "30 minutes before"
- Conferences: Currently "1 month before"

### Integration with Other Calendars

The system uses Fantastical's URL scheme. To adapt for other calendar apps:
1. Research the target app's URL scheme or API
2. Modify the URL generation in `/cal-sync` command
3. Update `SKILL.md` with new URL format

## System Requirements

- **macOS**: Required (Fantastical is macOS only)
- **Fantastical 3.x**: https://flexibits.com/fantastical
- **Python 3**: For parsing script (usually pre-installed on macOS)
- **Claude Code**: For command execution

## File Locations

**Commands:**
- `/cal-add`: `~/.claude/commands/cal-add.md`
- `/cal-sync`: `~/.claude/commands/cal-sync.md`

**Skill:**
- Main instructions: `~/.claude/skills/calendar-sync/SKILL.md`
- Parser script: `~/.claude/skills/calendar-sync/scripts/parse-dates.py`
- Template: `~/.claude/skills/calendar-sync/templates/planning-doc-template.md`
- Example: `~/.claude/skills/calendar-sync/examples/sample-project.md`

## Version History

**v1.0** (2025-11-03)
- Initial release
- Support for 4 item types: deadlines, milestones, meetings, conferences
- ISO and written date formats
- Recurring meeting support
- Batch processing with confirmation
- Comprehensive template and example

## Support

For issues with:
- **Calendar sync**: Check this README and try example file
- **Fantastical**: https://flexibits.com/support
- **Claude Code**: https://github.com/anthropics/claude-code/issues

---

**Author**: Claude (claude.ai/code)
**Date**: November 3, 2025
**Compatible with**: Fantastical 3.x, Claude Code, macOS
