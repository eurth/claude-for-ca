---
name: review
description: >
  Income tax compliance dispatcher. Shows pending ITR filings, advance tax due dates,
  notice deadlines, and lets the CA access any income tax skill quickly.
when_to_use: >
  At the start of a session when you want an income tax overview, to see what's due,
  or to quickly jump to any income tax skill.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_due_dates
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__list_notices
  - mcp__memory_bank__get_firm_profile
---

# Income Tax — Daily Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## Key Dates This Year

```
INCOME TAX CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
15 Jun  — Advance Tax 1st Instalment (15% of tax)
15 Sep  — Advance Tax 2nd Instalment (45% cumulative)
30 Sep  — Tax Audit Report (Form 3CA/3CB + 3CD) due
31 Oct  — ITR filing due (audit cases — businesses, professionals)
15 Dec  — Advance Tax 3rd Instalment (75% cumulative)
15 Mar  — Advance Tax 4th Instalment (100%)
31 Jul  — ITR for individuals (non-audit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available Income Tax Skills

```
/income-tax:itr-review          → Review ITR computation + 26AS/AIS check
/income-tax:advance-tax         → Calculate advance tax instalments
/income-tax:capital-gains       → Compute STCG/LTCG for all asset classes
/income-tax:tax-audit-3cd       → Form 3CA/3CB + 3CD clause-by-clause
/income-tax:notice-analysis     → Analyse and reply to IT notices
/income-tax:search-survey       → Search/survey emergency assistance
```

## Pending Notices and Action Items

Show any open income tax notices from memory bank.
