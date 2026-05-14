---
name: risk-matrix
description: >
  Prepare an audit risk matrix based on SA-315 (Understanding the Entity and Its
  Environment). Identify risks at financial statement level and assertion level.
  Maps risks to audit procedures, materiality thresholds, and working paper references.
when_to_use: >
  At the planning stage of an audit. Before developing the audit plan, prepare a risk
  matrix to identify significant risks and design appropriate audit responses.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Audit Risk Matrix — SA-315

**FINANCIAL INTEGRITY**: The risk assessment is the foundation of the entire audit. All significant risks must be identified and must have corresponding audit procedures. Skipping risks leads to audit failure and potential negligence liability for the firm.

## SA-315 Framework

SA-315 requires the auditor to:
1. Understand the entity and its environment
2. Identify risks of material misstatement (RMM) — inherent + control risk
3. Assess the risk of material misstatement at financial statement and assertion level
4. Identify "significant risks" requiring special audit attention

## Step 1 — Entity Understanding

Ask the CA to provide:
- **Industry**: Manufacturing / Trading / Services / NBFC / Real Estate etc.
- **Key financials**: Revenue, Total Assets, Profit/Loss
- **Ownership**: Promoter-controlled / PE-backed / Listed
- **Control environment**: Big 4 / mid-tier / in-house accounting
- **Prior year issues**: Any prior audit qualifications, restatements, frauds

## Step 2 — Materiality Setting

```
MATERIALITY CALCULATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Benchmark         | Percentage | Amount
Revenue           | 0.5–1%     | Rs.X,XX,XXX
Total Assets      | 0.5–1%     | Rs.X,XX,XXX
Profit Before Tax | 5–10%      | Rs.X,XX,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Selected Overall Materiality    : Rs.X,XX,XXX
Performance Materiality (75%)   : Rs.X,XX,XXX
Trivial / Clearly Inconsequential: Rs.XX,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 3 — Risk Matrix Template

| # | Area/Assertion | Risk Description | Inherent Risk | Control Risk | Combined RMM | Significant? | Audit Response | WP Ref |
|---|---|---|---|---|---|---|---|---|
| 1 | Revenue — Completeness | Sales not recorded / understated | High | Medium | High | YES | Cut-off procedures, post year-end sales testing | A-12 |
| 2 | Revenue — Occurrence | Fictitious revenues recorded | Medium | Low | Medium | No | Vouching large items > materiality | A-14 |
| 3 | Purchases — Completeness | Year-end accruals missing | High | Medium | High | YES | Cut-off, creditor reconciliation | B-10 |
| 4 | Inventory — Existence | Inventory overstated / phantom | Medium | High | High | YES | Physical verification, CARO Clause (ii) | C-01 |
| 5 | Fixed Assets — Valuation | Impairment not recognised | Medium | Medium | Medium | No | Market value comparison | D-05 |
| 6 | Related Party — Disclosure | Undisclosed related party txns | High | Low | High | YES | Director declarations, company search | E-08 |
| 7 | Contingent Liabilities | Pending litigations not disclosed | High | Low | High | YES | Management representation, legal letters | F-12 |
| 8 | Going Concern | Significant losses / NCA | Medium | Low | Medium | No | Cash flow review, post-audit events | G-01 |

## Step 4 — Significant Risks (SA-315.28)

Significant risks are those that require special audit consideration. Typically:
- Fraud risk (revenue manipulation, management override of controls)
- Complex estimates (fair value, ECL, provisions)
- Related party transactions outside normal course of business
- Unusual or infrequent transactions

For each significant risk: **Design specific audit procedures** beyond standard substantive testing.

```
SIGNIFICANT RISK RESPONSES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk: Revenue manipulation (fraud)
Response: 
  - Analytical review of monthly revenue (year-on-year, seasonal patterns)
  - Journal entry testing for unusual entries near year-end
  - Confirmation of top 10 customers' outstanding balances
  - Revenue recognition policy review + sample contracts

Risk: Related party transactions
Response:
  - Obtain complete list of related parties + reconcile with MCA filings
  - For each transaction > materiality: full vouching + commercial reasonability
  - Management representation letter — all related parties disclosed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 5 — Risk Matrix Summary

Generate audit programme assignments based on the risk matrix.
