---
name: review
description: >
  MCA / Secretarial compliance dispatcher. Shows pending ROC filings, upcoming AGM
  dates, and provides quick access to all MCA secretarial skills.
when_to_use: >
  At the start of a secretarial compliance session. To see pending filings,
  check due dates, or navigate to any MCA skill.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_due_dates
  - mcp__memory_bank__get_firm_profile
---

# MCA / Secretarial Compliance — Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## Key Annual Compliance Dates

```
ROC / MCA CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30 Sep   — AGM deadline (for Mar 31 FY companies)
30 Oct   — AOC-4 due (30 days after AGM)
29 Nov   — MGT-7/7A due (60 days after 30 Sep AGM)
30 Jun   — DPT-3 due (loans return)
30 Apr   — MSME-1 (H2 — Oct to Mar period)
31 Oct   — MSME-1 (H1 — Apr to Sep period)
30 Sep   — DIR-3 KYC for all directors
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Event-based: MGT-14 (30 days), CHG-1 (30 days), DIR-12 (30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available MCA / Secretarial Skills

```
/mca-secretarial:filing-tracker     → Track all pending ROC forms + late fee calc
/mca-secretarial:resolution         → Draft board/shareholder resolutions
/mca-secretarial:annual-compliance  → AGM notice, directors' report, annual return
/mca-secretarial:charge-registry    → CHG-1, CHG-4 — charge creation/satisfaction
```
