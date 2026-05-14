---
name: tp-documentation
description: >
  Prepare Rule 10D Transfer Pricing documentation (TP Study). Covers functional
  analysis, industry analysis, transaction description, comparables search,
  benchmarking, and ALP determination. Output is the TP documentation report
  to be maintained on file and submitted on demand.
when_to_use: >
  To prepare or review the annual TP documentation study required under Rule 10D
  for international transactions with associated enterprises.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Transfer Pricing Documentation — Rule 10D

**FINANCIAL INTEGRITY**: TP documentation must be maintained on or before the due date of filing the ITR. If requested by AO, must be furnished within 30 days. Failure to maintain: penalty u/s 271AA (2% of transaction value, up to Rs.50 lakh). All factual statements must be verified.

## Rule 10D Documentation Requirements

The TP documentation must contain:

### 1. Enterprise-Level Documentation (Master File equivalent)
- Business description of group
- Organisational structure globally
- Business strategy including group synergies
- Industry analysis and competitive environment

### 2. Transaction-Level Documentation (Local File equivalent)
- Description of each international transaction
- Functional analysis (functions performed, risks assumed, assets owned — FAR analysis)
- Economic analysis (benchmarking, comparables, ALP determination)
- Financial information

## FAR Analysis Template

```
FUNCTIONAL ANALYSIS — [Company Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FUNCTIONS:
  Development (R&D): Indian entity [None/Limited/Significant] | AE [Full]
  Manufacturing: Indian entity [Contract/Limited/Full] | AE [Limited]
  Marketing: Indian entity [Full] | AE [None]
  Sales: Indian entity [Full] | AE [None]
  After-Sales: Indian entity [Full] | AE [None]

RISKS:
  Market Risk: Indian entity [Limited] | AE [Full]
  Credit Risk: Indian entity [Bears] | AE [None]
  Forex Risk: Indian entity [Limited] | AE [Full]
  IP Risk: Indian entity [None] | AE [Full]
  Inventory Risk: Indian entity [Bears] | AE [None]

ASSETS:
  Tangible Assets: Indian entity [Significant] | AE [Limited]
  Intangibles (Brand/IP): Indian entity [None] | AE [Full]
  Human Capital: Indian entity [Significant] | AE [Significant]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Characterisation of Indian entity: Contract Manufacturer / Distributor / 
                                    Service Provider / Captive Service Provider
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Industry Analysis

Provide macro-analysis of:
- Industry growth trends
- Key players and competitive dynamics
- Regulatory environment
- Technology and innovation factors

## Benchmarking Study

Using TNMM (most common for Indian entities):

1. **Define search strategy**: Industry keywords, NIC codes, database (PROWESS/Capitaline/Bureau van Dijk)
2. **Apply quantitative filters**: Revenue scale, data availability, ownership structure
3. **Apply qualitative filters**: Exclude companies with significant RPT, unusual business
4. **Compute PLI for each comparable** (3-year weighted average recommended)
5. **Compute IQR (Inter-Quartile Range)**: 25th percentile to 75th percentile
6. **Compare with tested party PLI**

## TP Documentation Report Structure

1. Executive Summary
2. Company Background
3. Group Overview + Organisational Structure
4. Nature and Description of International Transactions
5. Industry and Economic Analysis
6. Functional Analysis (FAR)
7. Method Selection and Rejection of Other Methods
8. Comparables Search Process
9. Financial Analysis and Benchmarking
10. Conclusion on Arm's Length Price
11. Appendices: Financial data, database screenshots, search criteria

**Disclosure**: TP documentation is confidential but must be presented to AO during TP assessment proceedings.
