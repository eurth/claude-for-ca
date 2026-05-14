---
name: 26as-recon
description: >
  Reconcile Form 26AS TDS credits with the books of accounts. Match TDS deducted by
  payers with entries in income ledger, identify wrong PAN mappings, mismatched amounts,
  and TDS not reflected in 26AS. Prepare a summary for ITR filing.
when_to_use: >
  When the user wants to check if all TDS credits are properly reflected in 26AS,
  reconcile 26AS with books, identify missing TDS credits, or prepare TDS credit
  summary for ITR.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Form 26AS Reconciliation

**FINANCIAL INTEGRITY**: Only TDS appearing in 26AS can be claimed as a credit in the ITR. Claiming TDS not in 26AS leads to CPC adjustment (Section 143(1)) and demand. Conversely, unclaimed TDS in 26AS means the assessee paid taxes that are not being recovered.

## Step 1 — Download Form 26AS / AIS

**Form 26AS** — Available at: Income Tax e-filing portal → Services → Tax Statement (26AS)
**AIS (Annual Information Statement)** — More comprehensive, available on same portal

Ask user to download and share (or attach the PDF).

## Step 2 — Extract TDS Entries from 26AS

From Part A (TDS on salary) and Part B (TDS on other than salary):

| Sr. | Deductor Name | TAN | Gross Amount | TDS Deducted | TDS Deposited | Section | Remarks |
|---|---|---|---|---|---|---|---|
| 1 | [Employer] | [TAN] | Rs.X | Rs.X | Rs.X | 192 | |
| 2 | [Bank] | [TAN] | Rs.X | Rs.X | Rs.X | 194A | |

## Step 3 — Cross-Check with Books

Compare each 26AS entry with books:

| 26AS Entry | In Books? | Books Amount | Difference | Status |
|---|---|---|---|---|
| Salary from XYZ Ltd Rs.X | Yes | Rs.X | Rs.0 | ✓ Match |
| Interest from HDFC Rs.X | Yes | Rs.X | Rs.500 | ⚠ Difference |
| Rent from ABC Rs.X | No entry | — | Full amount | ⚠ Not in books |

## Step 4 — TDS in Books NOT in 26AS

These are cases where the payer deducted TDS but either:
- Did not deposit it to the government, OR
- Filed with wrong PAN, OR
- Return processing delay

For each such case:
- Draft letter to deductor requesting correction/deposit
- If large amount: consider approaching AO for manual TDS credit

## Step 5 — Common Issues and Resolutions

| Issue | Cause | Resolution |
|---|---|---|
| TDS in 26AS, no corresponding income in books | TDS on income not booked | Book the income and claim TDS |
| Income in books, TDS not in 26AS | Deductor not filed return / wrong PAN | Follow up with deductor |
| TDS amount in 26AS ≠ books | Different FY cut-off | Match dates carefully |
| Wrong TAN in 26AS | Deductor error | Contact deductor for correction |
| 26AS shows lower TDS than TDS certificate | Deductor filed incorrect return | Request TRACES correction |

## Step 6 — Reconciliation Summary

```
FORM 26AS RECONCILIATION — [Client] | PAN: [PAN] | FY: [FY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total TDS as per 26AS (all sections)    : Rs.X,XX,XXX
TDS matching with books                 : Rs.X,XX,XXX (N entries)
TDS in 26AS but not in books            : Rs.XX,XXX (N entries — book the income)
TDS in books but not in 26AS            : Rs.XX,XXX (N entries — follow up deductors)
Net claimable TDS credit in ITR         : Rs.X,XX,XXX (per 26AS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Action required before filing ITR:
[ ] Book [N] income items appearing in 26AS
[ ] Follow up [N] deductors for TDS deposit / PAN correction
[ ] Verify AIS for any additional income sources
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
