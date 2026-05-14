---
name: review
description: Payroll compliance dispatcher — overview and skill navigator
when_to_use: Start of a payroll session or to see due dates
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# Payroll Compliance — Dashboard

## Key Payroll Deadlines

```
PAYROLL COMPLIANCE CALENDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PF (EPF)     : Deposit by 15th of following month (EPFO portal)
ESIC         : Deposit by 15th of following month (esic.in)
TDS (192)    : Deposit by 7th of following month (Challan 281)
               March TDS: 30 April
Professional Tax: As per state (typically monthly by 31st)

PERIODIC:
PF ECR                : Monthly by 15th
ESIC Half-yearly      : By 11 Nov (Apr-Sep) / 12 May (Oct-Mar)
TDS Annual return 24Q : By 31 May (Q4)
Form 16               : Issue by 15 June
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available Payroll Skills

```
/payroll-compliance:pf-recon          → PF contribution, ECR generation
/payroll-compliance:esic-recon        → ESIC rates, monthly return
/payroll-compliance:professional-tax  → State-wise PT rates + return dates
```
