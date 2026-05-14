---
name: filing-tracker
description: >
  Track all mandatory MCA / ROC annual filings for companies — AOC-4, MGT-7/7A,
  MGT-14, ADT-1, DPT-3, MSME-1, BEN-2, INC-20A, and other event-based filings.
  Checks due dates, identifies overdue filings, and calculates late fees.
when_to_use: >
  To see all pending ROC filings for a company, calculate late fees for overdue
  filings, or plan the annual compliance calendar for a client.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - mcp__mca21__get_filing_status
  - Read
---

# MCA / ROC Filing Tracker

**FINANCIAL INTEGRITY**: ROC late filing attracts significant additional fees — starting at Rs.100/day with no ceiling for certain forms. Strike-off risk exists for companies with continuous default. All filings require CA/CS sign-off before submission.

## Annual Filing Calendar (Standard Private Company)

| Form | Purpose | Due Date | Frequency |
|---|---|---|---|
| AOC-4 | Financial Statements | Within 30 days of AGM (60 for OPC) | Annual |
| MGT-7 (Cos: Non-small) | Annual Return | Within 60 days of AGM | Annual |
| MGT-7A (Small Co) | Annual Return (small) | Within 60 days of AGM | Annual |
| ADT-1 | Appointment of Auditor | Within 15 days of AGM | Annual (first year) |
| MGT-14 | Filing of resolutions | Within 30 days of passing | Event-based |
| DPT-3 | Loans / Deposits Return | 30 June every year | Annual |
| MSME-1 | MSME Outstanding Payments | 30 Apr (Oct-Mar) / 31 Oct (Apr-Sep) | Half-yearly |
| BEN-2 | Significant Beneficial Owner | Within 30 days of declaration | Event-based |
| INC-20A | Commencement of Business | Within 180 days of incorporation | One-time |
| DIR-3 KYC / KYC Web | Director KYC | 30 September every year | Annual |
| LLP-11 | LLP Annual Return | 30 May | Annual (LLP) |
| LLP-8 | Statement of Accounts (LLP) | 30 October | Annual (LLP) |

## AGM Calendar

| Company Type | AGM Deadline | Note |
|---|---|---|
| First AGM | Within 9 months of incorporation or within 6 months of end of FY, whichever is earlier | |
| Subsequent AGMs | Within 6 months of end of FY — so by 30 Sep for Mar 31 FY | Maximum gap between AGMs: 15 months |
| OPC | Within 6 months of end of FY — AGM deemed conducted | |

## Late Fee Structure (as amended)

For most ROC forms under Companies Act 2013:
- Normal fee: As per schedule + late fee as below
- Up to 15 days late: 1× normal fee
- 16 to 30 days: 2× normal fee
- 31 to 60 days: 4× normal fee
- 61 to 90 days: 6× normal fee
- 91 to 180 days: 10× normal fee
- Beyond 180 days: 12× normal fee

For AOC-4 and MGT-7: Additional fee of Rs.100/day after expiry of extended period.

## Compliance Status Report

```
ROC FILING STATUS — [Company CIN] | [Company Name] | FY: [FY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGM Date (actual/planned): [date]
Auditor Name + Registration: [CA/CS]

ANNUAL FILINGS:
Form   | Due Date | Status           | Late Fee (if late)
AOC-4  | [date]   | ✓ Filed [date]   | Nil
MGT-7A | [date]   | ⚠ Pending        | Rs.X (X days late)
DPT-3  | 30-Jun   | ✓ Filed          | Nil
MSME-1 | 30-Apr   | ⚠ Overdue by N   | Rs.X × = Rs.X
DIR-3KYC | 30-Sep  | ✓ Done          | Nil

EVENT-BASED FILINGS (this year):
MGT-14 | Resolution for [XYZ] | Due [date] | ⚠ Pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIORITY: File [Form] immediately — additional late fee accruing at Rs.100/day
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
