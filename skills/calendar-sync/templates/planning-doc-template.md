# Project Planning Template

This template shows the recommended format for calendar items that can be automatically synced to Fantastical using `/cal-sync`.

## Project Information

**Project Name**: [Your project name]
**Start Date**: [YYYY-MM-DD]
**Principal Investigator**: [Your name]
**Status**: [Active/Planning/On Hold]

---

## Timeline

Use one of these formats for deadlines:

- **DUE: 2025-12-15 17:00** — Submit final manuscript to journal
- **Deadline: November 22, 2025 at 5pm** — IRB application due
- **Complete by December 1, 2025** — Finish data collection

> **Tip**: Deadlines automatically get "alert 1 week before"

---

## Milestones

Track progress with checkbox format:

- [ ] Complete literature review (by 2025-11-15)
- [ ] Finish MCMC implementation (2025-11-22)
- [ ] Draft results section (by 2025-11-30)
- [ ] Complete all analyses (2025-12-08)
- [ ] Manuscript first draft (by 2025-12-15)

> **Tip**: Milestones automatically get "alert 1 day before" and default to 9am

---

## Meetings

### Recurring Meetings

- **Weekly: Thursday 14:00** — Advisor check-in (Zoom)
- **Recurring Meeting: Lab meeting Friday 10:00** — Conference room B

> **Tip**: Recurring meetings automatically get "alert 30 minutes before"

### One-Time Meetings

- **Meeting: Collaborator discussion 2025-11-08 10:00** — Zoom
- **Call: Data analysis consultation 2025-11-15 at 2pm** — Phone

---

## Conferences & Events

### Academic Conferences

- **Conference: JSM 2025 (2025-08-02 to 2025-08-07)** — Seattle, WA
- **Event: BayesComp 2026 (2026-03-15 to 2026-03-20)** — Valencia, Spain

> **Tip**: Conferences automatically get "alert 1 month before"

### Workshops & Deadlines

- **DUE: 2025-05-01** — JSM abstract submission
- **DUE: 2025-06-15** — JSM early registration deadline

---

## Notes for Using This Template

### Date Formats Supported

**ISO Format** (recommended for precision):
```
2025-11-15
2025-11-15 14:30
```

**Written Format** (natural, but less precise):
```
November 15, 2025
Nov 15, 2025 at 2pm
```

**Recurring** (for meetings):
```
Every Thursday at 2pm
Weekly: Friday 10am
```

### Calendar Item Types

| Type | Format | Default Alert | Default Time |
|------|--------|---------------|--------------|
| Deadline | `DUE: [date]` or `Complete by [date]` | 1 week before | 5pm |
| Milestone | `- [ ] Task (by [date])` | 1 day before | 9am |
| Meeting | `Meeting: [title] [date time]` | 30 min before | Required |
| Conference | `Conference: [name] ([start] to [end])` | 1 month before | All-day |

### Best Practices

1. **Be explicit with dates**: Use ISO format (YYYY-MM-DD) to avoid ambiguity
2. **Include times for meetings**: Required for proper scheduling
3. **Add context in titles**: "Submit NSF grant" is better than "Submit grant"
4. **Location matters**: Include Zoom links or room numbers in descriptions
5. **Review before sync**: Run `/cal-sync` and review items before confirming

### Syncing This File

To sync calendar items from this file to Fantastical:

```
/cal-sync path/to/this-file.md
```

Or if you're in the same directory:

```
/cal-sync .
```

Claude will:
1. Parse all calendar items
2. Show you a summary table
3. Ask for confirmation
4. Create all events in Fantastical
5. Report results

---

## Example Complete Project

### Research Project: Bayesian Hierarchical Model for Clinical Trials

**Timeline**:
- **DUE: 2025-11-30** — Complete model specification document
- **DUE: 2025-12-15 17:00** — Submit manuscript to Statistics in Medicine
- **Complete by January 15, 2026** — Respond to reviewer comments

**Milestones**:
- [ ] Literature review complete (2025-11-08)
- [ ] Stan model implementation (by 2025-11-15)
- [ ] Simulation study complete (2025-11-22)
- [ ] Real data analysis (by 2025-11-29)
- [ ] Draft manuscript (2025-12-08)

**Regular Meetings**:
- **Weekly: Tuesday 10:00** — Research team meeting (Zoom)
- **Recurring Meeting: Thursday 14:00** — Advisor check-in (Office 423)

**Key Dates**:
- **Conference: ENAR 2026 (2026-03-08 to 2026-03-11)** — Baltimore, MD
- **DUE: 2025-12-01** — ENAR abstract submission
- **Meeting: Biostatistician consultation 2025-11-20 at 3pm** — Conference call

Running `/cal-sync` on this file would create:
- 3 deadlines (with 1 week alerts)
- 5 milestones (with 1 day alerts)
- 2 recurring meetings (with 30 min alerts)
- 1 conference (with 1 month alert)
- 2 additional one-time events

**Total: 13 calendar items**

---

## Troubleshooting

**No items found?**
- Check that dates are in supported formats
- Ensure keywords are present (DUE, Meeting, Conference)
- Verify file is valid markdown

**Wrong dates parsed?**
- Use ISO format (YYYY-MM-DD) for clarity
- Include year in all dates
- Be explicit with times (14:00 vs "2pm")

**Events not creating?**
- Ensure Fantastical is installed and running
- Check URL scheme permissions in macOS
- Try creating one event manually first with `/cal-add`

---

**Template Version**: 1.0
**Last Updated**: 2025-11-03
**Compatible with**: Fantastical 3.x
