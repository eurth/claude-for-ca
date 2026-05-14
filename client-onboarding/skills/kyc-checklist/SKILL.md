---
name: kyc-checklist
description: >
  Generate KYC (Know Your Customer) checklist for new clients. Covers individual,
  company, partnership firm, trust, and LLP KYC requirements. Includes PMLA
  (Prevention of Money Laundering Act) compliance checklist for CAs.
when_to_use: >
  When onboarding a new client. Use to generate the KYC document checklist,
  collect and verify documents, and ensure PMLA compliance.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__add_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# KYC Checklist — New Client Onboarding

**FINANCIAL INTEGRITY**: CAs are designated under PMLA (Prevention of Money Laundering Act). For certain transactions (company formation, property transactions, financial statement audits, trust/company management), CAs must conduct client KYC and maintain records. Non-compliance with PMLA can lead to prosecution.

## KYC Documents by Entity Type

### Individual Client

**Identity Proof (any one)**:
- [ ] PAN Card (mandatory)
- [ ] Aadhaar Card
- [ ] Passport
- [ ] Voter ID
- [ ] Driving License

**Address Proof (any one)**:
- [ ] Aadhaar Card (if not used as identity proof)
- [ ] Utility bill (not more than 3 months old)
- [ ] Bank statement (not more than 3 months old)
- [ ] Passport

**Financial Documents**:
- [ ] Last 2 ITRs with computation
- [ ] Bank account details (cancelled cheque / bank statement)

---

### Private / Public Limited Company

**Entity Documents**:
- [ ] Certificate of Incorporation
- [ ] MOA and AOA (latest version)
- [ ] PAN Card of company
- [ ] GST Registration Certificate (if applicable)
- [ ] Board Resolution authorising the engagement

**Directors**:
- [ ] PAN + Aadhaar of all directors
- [ ] DIN details of all directors
- [ ] List of directors from MCA portal (screenshot acceptable)

**Financial**:
- [ ] Last 2 years' audited financial statements
- [ ] Latest bank statement (3 months)

---

### Partnership Firm / LLP

- [ ] Partnership Deed / LLP Agreement
- [ ] PAN Card of firm
- [ ] PAN + Aadhaar of all partners
- [ ] Certificate of Registration (LLP) from MCA
- [ ] GST Registration

---

### Trust / NGO

- [ ] Trust Deed / Bye-laws
- [ ] Registration certificate (Societies Registration Act / Trust Act)
- [ ] 12A / 80G registration certificate (FCRA if foreign funds)
- [ ] PAN of trust
- [ ] List of trustees / governing body members with KYC

---

## PMLA Compliance for CAs

CAs are "Reporting Entities" under PMLA when engaged in:
1. Formation of companies, LLPs, trusts
2. Audit / accountancy / financial management for clients
3. Real estate transactions (buying/selling on behalf of client)
4. Management of client funds / bank accounts

**Obligations**:
- Conduct CDD (Customer Due Diligence) before starting engagement
- Maintain KYC records for 5 years after end of engagement
- File Suspicious Transaction Report (STR) if any suspicious activity detected
- Report Cash Transactions > Rs.10 lakh per transaction

## Client Onboarding Record

```
CLIENT ONBOARDING LOG — [Client Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date of onboarding  : [date]
Client type         : Individual / Company / LLP / Firm / Trust
PAN                 : [XXXXX]
GSTIN               : [if applicable]
Engagement type     : Audit / Accounting / GST / Advisory
Engagement letter   : Signed on [date] | Ref: [EL-XXXX]
KYC documents       : Collected ✓ / Pending ✗
PMLA CDD completed  : Yes / No
Referred by         : [if any]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
