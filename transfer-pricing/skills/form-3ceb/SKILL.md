---
name: form-3ceb
description: >
  Assist with preparation and review of Form 3CEB — the Transfer Pricing Audit Report
  to be filed by a Chartered Accountant. Covers all 25+ paragraphs, international
  transactions, specified domestic transactions, and method selection.
when_to_use: >
  When preparing or reviewing Form 3CEB for a company with international transactions
  or specified domestic transactions exceeding the threshold.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Form 3CEB — Transfer Pricing Audit Report

**FINANCIAL INTEGRITY**: Form 3CEB is signed by a CA and has significant legal consequences. Every certification must be supported by documented evidence. ALP (Arm's Length Price) determination requires proper benchmarking — incorrect certification leads to TP adjustments + 2× penalty on the adjustment amount.

## Applicability Thresholds

**International Transactions (Section 92)**:
- Every company with international transactions with AEs must file Form 3CEB
- No minimum threshold — even Rs.1 transaction requires filing
- Due date: 31 October (same as ITR for audit cases)

**Specified Domestic Transactions (Section 92BA)**:
- Transactions with domestic related parties exceeding Rs.20 crore in aggregate during FY

## Transfer Pricing Methods (Section 92C / Rule 10B)

| Method | Full Name | Best Used For |
|---|---|---|
| CUP | Comparable Uncontrolled Price | Commodity transactions, financial transactions |
| RPM | Resale Price Method | Distribution / resale without value-add |
| CPM | Cost Plus Method | Manufacturing, contract services |
| PSM | Profit Split Method | Highly integrated businesses, global products |
| TNMM | Transactional Net Margin Method | **Most commonly used** — services, manufacturing |

## Form 3CEB Paragraph Coverage

### Part A — General Information
- Para 1-4: Company details, AE relationships, nature of business

### Part B — International Transactions
**Para 5-10**: Tangible property sale/purchase
**Para 11-13**: Services — intragroup services, technical services
**Para 14-15**: Intangibles — royalties, technical know-how, brand
**Para 16**: Financial transactions — loans, guarantees, etc.
**Para 17**: Business restructuring (transfer of business, functions, risks)
**Para 18-20**: Other international transactions

### Part C — Specified Domestic Transactions
**Para 21-25**: Transactions with domestic related parties (if SDT applicable)

## Standard TNMM Analysis

**Step 1 — Select Tested Party**
- Less complex entity: Usually the Indian entity (service provider, manufacturer)
- Tested party should be the entity performing routine functions

**Step 2 — Define Profit Level Indicator (PLI)**
- Operating Profit Margin (OP/Net Revenue) — for services
- ROCE (Return on Capital Employed) — for manufacturing
- Gross Margin — for distribution

**Step 3 — Database Search (PROWESS / Capitaline)**
```
SEARCH CRITERIA:
Industry: [NIC Code / Industry Description]
Financial years: [Current FY + 2 prior years]
Criteria:
  - Comparable company in same industry
  - Minimum 3 years of data
  - Revenue scale comparable to tested party (25%–400% filter)
  - No significant related party transactions (< 25% of revenue)
  - No losses for 2+ consecutive years
  - Publicly available financial data
```

**Step 4 — Compute Arm's Length Range**
```
COMPARABLES:
Company      | FY1 PLI | FY2 PLI | FY3 PLI | Average
Comp A       | 12.5%   | 14.2%   | 11.8%   | 12.8%
Comp B       | 8.3%    | 9.1%    | 7.6%    | 8.3%
[etc.]

Arm's Length Range (IQR): [X%] to [Y%]
Tested Party Margin: [Z%]
Status: ✓ Within range / ⚠ Below range (adjustment required)
```

**Step 5 — Form 3CEB Reporting**

For each transaction paragraph:
```
Para [X] — International Transaction:
Description: [X type services rendered to AE Y]
Amount: Rs.X,XX,XXX
Method: TNMM
Arm's Length Price: Rs.X,XX,XXX
Actual Price charged: Rs.X,XX,XXX
Variation: [Nil / Rs.X — within +/- 3% tolerance]
Opinion of CA: The price is at arm's length / not at arm's length
```

## TP Adjustment and Penalty

If TP adjustment made:
- Tax on adjustment: 30% × adjustment amount
- Interest u/s 234B/234C on underpayment
- Penalty u/s 271(1)(c): 100%-300% of tax
- Penalty u/s 271G (for failure to maintain TP documentation): 2% of transaction value
- Penalty u/s 271AA (for failure to maintain TP documentation): 2% of transaction value
