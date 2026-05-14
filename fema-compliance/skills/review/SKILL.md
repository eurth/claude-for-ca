---
name: review
description: FEMA compliance dispatcher — overview and skill navigator
when_to_use: Start of a FEMA session or to see due dates and navigate to FEMA skills
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# FEMA Compliance — Dashboard

## Key FEMA Deadlines

```
FEMA / RBI COMPLIANCE CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FC-GPR    : Within 30 days of share allotment
FC-TRS    : Within 60 days of share transfer
FLA Return: 15 July (all entities with FDI or ODI)
APR       : 31 May (entities that have made ODI)
FCGPR Annual Return: As part of FLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: All FEMA filings through FIRMS portal (RBI): firms.rbi.org.in
      FLA Return: flair.rbi.org.in
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available FEMA Skills

```
/fema-compliance:fdi-compliance   → FC-GPR, FC-TRS, FDI checklist, pricing norms
/fema-compliance:odi-compliance   → ODI reporting, APR annual return
```
