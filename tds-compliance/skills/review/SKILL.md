---
name: review
description: >
  TDS/TCS compliance dispatcher. Shows TDS defaults, upcoming quarterly return due dates,
  26AS reconciliation status, and provides quick access to all TDS skills.
when_to_use: >
  At the start of a TDS session to see what's pending, check default status,
  or navigate to any TDS skill.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_due_dates
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# TDS/TCS — Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## Quarterly Return Due Dates

```
TDS RETURN CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q1 (Apr-Jun)  → Return due: 31 July   | Form 16A by: 15 Aug
Q2 (Jul-Sep)  → Return due: 31 Oct    | Form 16A by: 15 Nov
Q3 (Oct-Dec)  → Return due: 31 Jan    | Form 16A by: 15 Feb
Q4 (Jan-Mar)  → Return due: 31 May    | Form 16 by: 15 Jun
              (Monthly TDS deposit: 7th of next month)
              (March: deposit by 30 Apr)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available TDS Skills

```
/tds-compliance:default-check       → Detect late/short/non-deduction defaults + 201(1A) interest
/tds-compliance:26as-recon          → Reconcile 26AS with books
/tds-compliance:form-16-generator   → Prepare Form 16 Part B / Form 16A
/tds-compliance:quarterly-return    → Review and file 24Q/26Q return
```

## Quick Reference — TDS Deposit Due Dates

- Monthly TDS (all deductions): 7th of the following month
- March deduction: 30th April (not 7th May)
- Payments to government: Same day as deduction
