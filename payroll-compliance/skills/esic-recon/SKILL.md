---
name: esic-recon
description: >
  Review and reconcile ESIC (Employees State Insurance Corporation) contributions.
  Covers ESI rate (employer 3.25% + employee 0.75%), wage ceiling (Rs.21,000/month),
  half-yearly return filing, and health card registration.
when_to_use: >
  When reviewing monthly ESIC compliance, generating ESIC challan,
  or filing the half-yearly ESIC return.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
---

# ESIC — Monthly Compliance

**FINANCIAL INTEGRITY**: ESI is applicable to employees with gross wages ≤ Rs.21,000/month (Rs.25,000 for persons with disability). Once an employee is covered in a contribution period, they remain covered for the full benefit period even if wages exceed Rs.21,000 mid-year.

## ESI Contribution Rates

| Contribution | Rate |
|---|---|
| Employer contribution | 3.25% of gross wages |
| Employee contribution | 0.75% of gross wages |
| **Total** | **4.00%** of gross wages |

**Note**: Employees earning ≤ Rs.137/day (approx.) are exempt from employee contribution — only employer pays.

## ESI Contribution Periods

| Period | Contribution Due For | Benefit Period |
|---|---|---|
| April 1 — September 30 | October 1 — March 31 |
| October 1 — March 31 | April 1 — September 30 |

## Monthly ESI Payment

- Due date: 15th of the following month
- Payment through ESI portal: esic.in → employer login

```
ESIC REGISTER — [Month] [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Emp No | Name   | IP No.     | Gross Wages | Emp ESI | Er ESI | Total
E001   | Ravi K | 1234567890 | 18,000      | 135     | 585    | 720
E002   | Priya  | 1234567891 | 20,000      | 150     | 650    | 800
E003   | Amit S | Not cov.   | 22,000      | —       | —      | — (exceeds ceiling)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL ESI contribution this month: Rs.X,XXX
Due by: 15 [Next Month]
```

## Half-Yearly Return

- **Contribution Period April–September**: Return by 11 November
- **Contribution Period October–March**: Return by 12 May
- Filed through ESIC portal: employer uploads employee wage data
