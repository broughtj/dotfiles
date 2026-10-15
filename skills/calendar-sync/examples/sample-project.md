# Sample Project: Monte Carlo Methods for Bayesian Inference

This is an example project planning document showing how to format calendar items for automatic syncing with Fantastical.

## Project Overview

**Principal Investigator**: Dr. Research Scientist
**Start Date**: 2025-11-01
**Expected Completion**: 2025-12-31
**Funding**: NSF Grant #12345

## Research Goals

Develop novel adaptive MCMC algorithms for high-dimensional Bayesian hierarchical models with application to longitudinal clinical trial data.

---

## Timeline & Deadlines

### Phase 1: Literature & Design (Weeks 1-2)

- **DUE: 2025-11-15** — Complete literature review document
- **DUE: 2025-11-18 17:00** — Submit IRB protocol revision

### Phase 2: Implementation (Weeks 3-5)

- **Deadline: November 29, 2025 at 5pm** — Finish Julia implementation
- **Complete by December 6, 2025** — Complete simulation study

### Phase 3: Writing & Submission (Weeks 6-8)

- **DUE: 2025-12-13** — First manuscript draft
- **DUE: 2025-12-20 17:00** — Submit to Journal of Computational Statistics
- **DUE: 2025-12-27** — Prepare conference presentation

---

## Milestones Checklist

### Implementation

- [ ] Set up Julia project environment (by 2025-11-08)
- [ ] Implement basic MCMC sampler (2025-11-12)
- [ ] Add adaptive tuning mechanism (by 2025-11-15)
- [ ] Implement parallel chains (2025-11-18)
- [ ] Add convergence diagnostics (by 2025-11-22)

### Analysis

- [ ] Design simulation scenarios (by 2025-11-20)
- [ ] Run preliminary simulations (2025-11-25)
- [ ] Complete full simulation study (by 2025-12-02)
- [ ] Analyze real data (2025-12-06)
- [ ] Generate all figures and tables (by 2025-12-09)

### Writing

- [ ] Draft methods section (by 2025-11-27)
- [ ] Draft results section (2025-12-04)
- [ ] Complete introduction and discussion (by 2025-12-11)
- [ ] Internal review complete (2025-12-16)
- [ ] Final revisions (by 2025-12-19)

---

## Meetings & Collaborations

### Regular Meetings

- **Weekly: Thursday 14:00** — Advisor progress check-in (Zoom)
- **Recurring Meeting: Tuesday 10:00** — Research team meeting (Conference Room B)
- **Weekly: Friday 15:00** — Computational methods lab meeting

### Scheduled Consultations

- **Meeting: Biostatistics consult 2025-11-10 at 10:00** — Discuss trial design
- **Call: Collaborator check-in 2025-11-17 at 2pm** — Review preliminary results
- **Meeting: IRB follow-up 2025-11-20 at 3pm** — Address protocol questions
- **Meeting: Final manuscript review 2025-12-15 at 10am** — With advisor

---

## Conferences & Travel

### Upcoming Conferences

- **Conference: JSM 2026 (2026-08-01 to 2026-08-06)** — Philadelphia, PA
- **Event: MCMSki 2026 (2026-01-05 to 2026-01-09)** — Virtual

### Conference Deadlines

- **DUE: 2026-02-01** — JSM abstract submission
- **DUE: 2026-03-15** — JSM early registration
- **DUE: 2025-11-30** — MCMSki presentation submission

---

## Grant & Administrative

### Reporting

- **DUE: 2025-12-31** — NSF annual progress report
- **Complete by December 20, 2025** — Update project website

### Travel

- **Meeting: Lab retreat 2025-11-22 at 9am** — All-day event, campus center

---

## Notes

### Random Seeds
Remember to document all random seeds for reproducibility:
- Simulation study: seed = 2025
- Real data analysis: seed = 12345

### Software Versions
- Julia 1.10.0
- Turing.jl v0.30.0
- MCMCDiagnosticTools.jl v0.3.0

### Data Files
- Raw data: `data/raw/clinical-trial-2025.csv`
- Processed: `data/processed/analysis-ready.csv`

---

## Calendar Sync Summary

This file contains:
- **9 hard deadlines** (submissions, reports, documents)
- **15 milestones** (implementation and writing tasks)
- **3 recurring meetings** (weekly check-ins)
- **4 one-time meetings** (consultations and reviews)
- **2 conferences** (with 3 associated deadlines)

**Total: 33 calendar items**

To sync all items to Fantastical:
```
/cal-sync sample-project.md
```

Or test with just deadlines by running the Python script directly:
```bash
python3 ~/.claude/skills/calendar-sync/scripts/parse-dates.py sample-project.md
```
