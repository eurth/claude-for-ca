---
name: articleship-log
description: >
  Manage articleship diary and practical training log for CA students. Tracks
  hours by area (audit, accounts, taxation, corporate laws), generates weekly/monthly
  diary entries, monitors ICAI prescribed area-wise minimums, and prepares the
  articleship completion certificate data.
when_to_use: >
  For CA students to log their daily articleship work, get weekly diary entry
  drafts, check area-wise completion status, or prepare for practical training
  assessment.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Articleship Diary — CA Student

## ICAI Practical Training — Required Hours

Total articleship: 3 years (156 weeks / ~1,095 days excluding leaves)

ICAI stipulates minimum hours in the following areas (indicative — check latest ICAI guidelines):

| Area | Minimum Hours |
|---|---|
| Accounting | 100 hours |
| Auditing | 200 hours |
| Direct Tax | 150 hours |
| Indirect Tax / GST | 100 hours |
| Corporate Laws | 100 hours |
| FEMA / Other Laws | 50 hours |
| Information Technology | 100 hours |
| Other Work | Remaining hours |

## Daily Work Log Entry

For each day's work, provide:
- Date
- Work description
- Area (Accounting / Audit / Direct Tax / Indirect Tax / Corporate Laws / Other)
- Hours worked
- Supervisor name

Example input:
```
Date: 15-May-2026
Work: Assisted in preparation of GSTR-3B reconciliation for [Client Name]
Area: Indirect Tax
Hours: 6
Supervisor: CA [Name]
```

Output — Diary Entry:
```
DATE: 15th May 2026 | AREA: Indirect Tax
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Work performed: Assisted in reconciliation of GSTR-3B with books of accounts for
a manufacturing client. Compared output tax liability (B2B, B2C, export), ITC
(IGST, CGST, SGST), and net tax payable with ledger entries. Identified differences
in ITC claims related to ineligible items under Section 17(5). Prepared reconciliation
statement showing monthly difference for Q4 of FY 2025-26.

Supervised by: CA [Name], M.No.: [XXXXXX]
Hours: 6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Area-wise Hours Tracker

```
ARTICLESHIP HOURS TRACKER — [Student Name] | Started: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Area             | Completed | Required | Status
Accounting       | 80 hrs    | 100 hrs  | 20 hrs pending
Auditing         | 150 hrs   | 200 hrs  | 50 hrs pending
Direct Tax       | 140 hrs   | 150 hrs  | 10 hrs pending
Indirect Tax     | 85 hrs    | 100 hrs  | 15 hrs pending
Corporate Laws   | 60 hrs    | 100 hrs  | 40 hrs pending
FEMA/Other Laws  | 45 hrs    | 50 hrs   | 5 hrs pending
IT               | 100 hrs   | 100 hrs  | ✓ Done
Other Work       | 200 hrs   | —        | —
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total logged: 860 hrs | Projected completion: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ICAI Form 112 (Articleship Registration) Reminder

- Register within 30 days of joining the firm
- ICAI portal: self-service.icai.org
- Form 103: Registration of articleship
- Form 109: Termination (if switching firms)
- Form 108: Completion of articleship
