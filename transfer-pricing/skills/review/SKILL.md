---
name: review
description: Transfer pricing compliance dispatcher — overview and skill navigator
when_to_use: Start of a TP session or to navigate to TP skills
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# Transfer Pricing — Dashboard

## Key TP Deadlines

```
TRANSFER PRICING CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
30 Sep  — Maintain TP documentation (Rule 10D) by this date
31 Oct  — Form 3CEB filing (with ITR for TP cases)
          (Country-by-Country Report — 12 months after end of reporting FY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Threshold: All international AE transactions → 3CEB mandatory
SDT threshold: Domestic related party transactions > Rs.20 Cr
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available TP Skills

```
/transfer-pricing:form-3ceb         → Form 3CEB preparation + TNMM benchmarking
/transfer-pricing:tp-documentation  → Rule 10D TP documentation study
```
