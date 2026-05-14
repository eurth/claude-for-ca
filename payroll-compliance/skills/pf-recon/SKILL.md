---
name: pf-recon
description: >
  Reconcile and review Provident Fund (PF/EPF) compliance. Covers ECR (Electronic
  Challan cum Return) generation, PF contribution rates (employer 12% / employee 12%),
  split of employer contribution (EPS 8.33% / EPF 3.67%), new joiner/exit handling,
  and EPFO portal compliance.
when_to_use: >
  When reviewing monthly PF compliance, preparing ECR for EPFO portal,
  or reconciling PF liability with salary register.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Provident Fund (EPF) — Monthly Compliance

**FINANCIAL INTEGRITY**: PF contribution is a trust liability — employee contribution deducted from salary MUST be deposited with EPFO. Failure to deposit (even if deducted) is a criminal offence under EPF Act. Always ensure deposit by the 15th of the next month.

## PF Contribution Rates

| Contribution | Rate | Based On |
|---|---|---|
| Employee contribution (EPF) | 12% | Basic + DA |
| Employer contribution (total) | 12% | Basic + DA |
| ↳ EPS (Employee Pension Scheme) | 8.33% (max Rs.1,250/month) | Basic + DA (capped at Rs.15,000) |
| ↳ EPF employer portion | 3.67% (+ excess if salary > Rs.15,000) | Basic + DA |
| EDLI (Employee Deposit Linked Insurance) | 0.50% | Basic + DA (capped at Rs.15,000) |
| Admin / EPFO admin charges | 0.50% (min Rs.75/month) | EPF wages |

**Note**: If employee's Basic + DA > Rs.15,000, contribution is on actual salary (not capped at Rs.15,000) unless both employer and employee agree to cap at Rs.15,000.

## Monthly PF Reconciliation

For each employee:

```
PF REGISTER — [Month] [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emp No | Name     | UAN       | Basic+DA | Empl EPF | Empl EPS | Empl EDLI | Total
E001   | Ravi K   | 101234567 | 25,000   | 3,000    | 1,250    | 75        | 4,325
E002   | Priya M  | 101234568 | 15,000   | 1,800    | 1,250    | 75        | 3,125
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total employee deduction : Rs.X,XXX
Total employer contribution: Rs.X,XXX
EDLI total              : Rs.XXX
Admin charges           : Rs.XXX
TOTAL TO DEPOSIT        : Rs.X,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Challan due: 15th of following month (e.g., May contributions → 15 June)
```

## ECR (Electronic Challan cum Return)

The ECR is filed through the EPFO employer portal (unified.epfindia.gov.in):
1. Download ECR template
2. Fill: UAN, employee name, EPF wages, EPS wages, EPF/EPS/EDLI contributions
3. Upload to portal → Generate Challan
4. Pay via net banking / NEFT
5. Download payment receipt + TRRN (Transaction Reference Number)

## New Joiners / Exits

**New joiner**: Register on EPFO portal before first ECR filing with UAN number.
- If no previous PF: Generate UAN on portal
- If existing UAN: Link to employer through portal

**Exit / Full and Final Settlement**:
- File exit date on EPFO portal
- Employee can claim PF after 2 months of exit (Form 19 + Form 10C)
- Transfer PF to new employer's trust / EPFO (Form 13)

## PF Compliance Checklist

```
[ ] Salary register prepared for the month
[ ] PF deduction computed on correct Basic + DA
[ ] New joiners registered / exited employees closed
[ ] ECR uploaded on EPFO portal
[ ] Challan generated and payment made by 15th
[ ] TRRN downloaded and filed
[ ] Passbook entries updated on EPFO member portal
```
