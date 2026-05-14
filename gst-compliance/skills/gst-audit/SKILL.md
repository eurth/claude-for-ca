---
name: gst-audit
description: >
  GST Audit assistance under Section 35(5)/Section 65/66. Covers departmental audit
  (Section 65) representation and special audit (Section 66). Also assists with
  GST annual audit checklist, ITC reversal calculations, and reconciliation for
  audit submissions.
when_to_use: >
  When a client receives a GST audit notice (Section 65/66), or when the CA needs to
  prepare for a GST audit, or conduct an internal GST audit review for a client.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__log_notice
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# GST Audit Assistance

**FINANCIAL INTEGRITY**: GST audit proceedings carry significant legal risk. All representations must be reviewed and signed by a qualified CA/advocate. Audit findings can result in large demands, interest, and penalties. Nothing is submitted without partner sign-off.

## Section 65 vs Section 66 Audit

| Feature | Section 65 | Section 66 |
|---|---|---|
| Type | Departmental Audit | Special Audit by CA/CMA |
| Who conducts | GST officers | CA / CMA appointed by Commissioner |
| Trigger | Routine or risk-based | Where accounts are complex / suspected evasion |
| Notice | FORM GST ADT-01 | FORM GST ADT-03 |
| Period | Within 3 months (extendable to 6M) | Within 90 days (extendable) |
| Reply | FORM GST ADT-02 | FORM GST ADT-04 |

## GST Audit Checklist — Areas of Scrutiny

### 1. Registration and Profile
- [ ] Registration certificate validity (active/cancelled)
- [ ] Correct entity type and HSN/SAC
- [ ] Authorised signatory current
- [ ] Business address matches records

### 2. Outward Supplies
- [ ] Revenue per books vs GSTR-1 (annual reconciliation)
- [ ] E-invoice compliance (if applicable)
- [ ] Advances received — GST on time-of-supply
- [ ] Reverse charge correctly identified and discharged
- [ ] Zero-rated exports: LUT validity / IGST payment
- [ ] Related party transactions at arm's length value

### 3. Input Tax Credit
- [ ] Section 16 conditions: tax invoice, receipt, supplier filing, payment
- [ ] Section 17(5) blocked credits: none claimed in ineligible categories
- [ ] Rule 42/43 reversals: proportionate reversal if exempt supplies
- [ ] GSTR-2B reconciliation: ITC not in excess of GSTR-2B
- [ ] Capital goods: correct classification and reduced ITC %

### 4. Returns and Payments
- [ ] All returns filed (no missed months)
- [ ] Tax paid by due date (no interest outstanding)
- [ ] Late fees paid where applicable
- [ ] PMT-06 challans for QRMP filers

### 5. E-way Bill Compliance (for goods movement)
- [ ] E-way bills generated for all consignments > Rs.50,000
- [ ] Validity not expired at time of movement
- [ ] Vehicle number updated in EWB

### 6. RCM (Reverse Charge Mechanism)
- [ ] GTA services — RCM discharged at 5% on freight paid
- [ ] Import of services — IGST under RCM
- [ ] Legal services from individual advocates
- [ ] Security services from unregistered persons
- [ ] Rent from government entities

### 7. TDS/TCS under GST (if applicable)
- [ ] TDS deducted on govt contracts > Rs.2.5L (Section 51)
- [ ] TCS collected on e-commerce sales (Section 52)
- [ ] Reflected in electronic cash ledger

## Audit Representation Package

### Documents to Prepare
1. Registration certificate + amendments
2. Annual turnover certificate
3. Books of accounts (electronic records: Tally/ERP)
4. GSTR-1, 3B, 9 for audit period
5. GSTR-2B downloads for all months
6. Purchase register + sales register
7. Bank statements
8. Inward / outward supply reconciliation statement
9. ITC register with supporting invoices
10. Explanation for any differences identified

### Draft Response to FORM GST ADT-01

```
[Firm Letterhead]
Date: [date]

To,
The [Superintendent / Assistant Commissioner]
[Office Address]

Sub: Response to Notice in FORM GST ADT-01 dated [date] — [Client Name] | GSTIN [GSTIN]

Sir/Madam,

With reference to the above-mentioned notice for GST audit of [Client Name] for the
period [period], we hereby acknowledge the same and confirm the following:

DOCUMENTS AVAILABLE FOR AUDIT:
- Books of accounts maintained in: [Tally Prime / other software]
- Period covered: [FY start to end]
- Location: [office address] / [shared digitally via secure folder]

AUDIT SCHEDULE PREFERENCE:
We request that the audit be scheduled for: [proposed dates]
Contact person: [name, phone, email]

We assure full cooperation during the audit proceedings.

Yours faithfully,
[CA Name] [Membership No.]
[Firm Name]
```

## Post-Audit — Reply to FORM GST ADT-02

If the audit results in a demand / observation:
- Review each para of ADT-02 carefully
- Identify: agreed items (pay via DRC-03) and disputed items
- File a detailed written reply para-by-para with supporting documents
- If demand > Rs.5 Lakh and dispute genuine, consider filing an appeal (Form APL-01)

## ITC Calculation for Audit Findings

If auditors find excess ITC claimed, calculate:
- Principal ITC reversal
- Interest @ 24% per annum from date of claim to date of payment (Section 50)
- Penalty — equal to tax amount if fraud; 10% (minimum Rs.10,000) if not fraud

```
EXCESS ITC CALCULATION (for payment via DRC-03):
Excess ITC claimed: Rs.X
Interest @ 24% from [date of GSTR-3B] to [today]: Rs.X
Total payable via DRC-03: Rs.X

Recommendation: Pay DRC-03 immediately to stop interest accrual.
```
