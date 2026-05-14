---
name: internal-audit
description: >
  Internal audit planning and reporting. Covers risk-based internal audit plan,
  process-level audit (procurement, payroll, cash, revenue cycle), control testing,
  Internal Audit Report (IAR) drafting, and follow-up on prior period recommendations.
when_to_use: >
  When conducting or reviewing an internal audit. Use to plan the audit scope,
  document control testing, and draft the internal audit report.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Internal Audit — Planning and Reporting

**FINANCIAL INTEGRITY**: Internal audit findings must be objective and based on evidence. Recommendations should be practical and implementable. The audit report is shared with management and the Audit Committee — accuracy and tone are critical.

## Internal Audit Plan (Risk-Based)

### Universe of Auditable Areas (Standard Template)

| Process | Risk Level | Frequency | Last Audit |
|---|---|---|---|
| Revenue / Debtors | High | Quarterly | [date] |
| Procurement / Payables | High | Quarterly | [date] |
| Payroll | High | Half-yearly | [date] |
| Cash and Bank | High | Monthly | [date] |
| Fixed Assets | Medium | Annually | [date] |
| Inventory | Medium | Quarterly | [date] |
| IT / System Access | High | Annually | [date] |
| Contracts & Agreements | Medium | Annually | [date] |
| Statutory Compliance | High | Quarterly | [date] |

## Revenue Cycle Audit

**Objectives**: Revenue completeness, accurate billing, proper approvals, timely collection

**Key Controls to Test:**
- [ ] All sales orders authorised before dispatch
- [ ] Dispatch = Invoice = Recording — no gaps or duplicates
- [ ] Credit limit approval for new customers
- [ ] Collection received matched to invoice, no unapplied credits
- [ ] Unusually large/round-number transactions reviewed by senior management
- [ ] Credit notes require approval — no unauthorised credits

## Procurement Cycle Audit

**Objectives**: Authorised purchases, competitive procurement, correct recording, timely payment

**Key Controls:**
- [ ] Purchase orders raised against approved requisitions only
- [ ] 3-way match: PO + Goods Receipt + Invoice before payment
- [ ] Vendor master changes require separate approval
- [ ] Related party purchases disclosed
- [ ] Advance to vendors within approved limits; advances reconciled

## Payroll Audit

**Objectives**: Payroll completeness and accuracy, authorised changes, PF/ESI/TDS compliance

**Key Controls:**
- [ ] Joiner/leaver list from HR matches payroll system
- [ ] Salary changes require HR approval letter
- [ ] PF/ESI deduction and deposit — amounts correct and timely
- [ ] TDS computation verified against Form 16 data
- [ ] Unclaimed wages transferred to unpaid wages account (not cash/bank directly)
- [ ] Overtime: approved and rate correct

## Internal Audit Report Format

```
INTERNAL AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client: [Name] | Period: [Q/FY] | Report Date: [date]
Audit Area: [Revenue / Payroll / etc.] | Conducted by: [Staff]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTIVE SUMMARY:
[2-3 line summary of overall findings and control environment]

DETAILED FINDINGS:

Finding #1: [Title]
Risk Level: HIGH / MEDIUM / LOW
Observation: [Factual description of what was found]
Impact: [Financial or operational impact]
Root Cause: [Why this happened — process / system / people]
Recommendation: [Specific, actionable recommendation]
Management Response: [Management's action plan + target date]
Status: Open

[Repeat for each finding]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY TABLE:
High Risk Findings: [N]
Medium Risk Findings: [N]
Low Risk Findings: [N]
Prior period items closed: [N]
Prior period items still open: [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
