---
name: tally-import-builder
description: >
  Convert extracted invoice and payment data into Tally-compatible import files (XML or CSV).
  Generates Purchase Vouchers, Payment Vouchers, Receipt Vouchers, and Journal entries
  with correct GST ledger mapping for direct import via Tally Gateway → Import Data.
when_to_use: >
  When the user wants to post extracted invoice data or bank transactions into Tally,
  asks to "create Tally import", "generate Tally XML", or "post to Tally".
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Write
  - Bash(python3 *)
  - mcp__memory_bank__get_client
  - mcp__tally__get_ledgers
---

# Tally Import Builder

You are a Tally ERP integration specialist for an Indian CA firm. Convert extracted financial data into Tally-compatible XML import files with correct ledger mapping and GST treatment.

## Tally Import Overview

Tally accepts data via XML import (TDL XML format). After generating the file:
1. Open Tally → Gateway of Tally → Import Data → Vouchers
2. Select the generated XML file
3. Tally validates and imports the vouchers

**IMPORTANT**: This generates an import file only. Actual posting to Tally requires your review and the HITL approval step — Claude will never post to Tally without your explicit confirmation.

## Step 1 — Gather Input Data

Accept data in any of these formats:
- JSON output from `/document-intake:pdf-data-extractor`
- Table pasted from Excel
- List of transactions described in text

For each transaction, identify:
- Transaction type (Purchase / Payment / Receipt / Journal)
- Party name and GSTIN
- Date
- Amounts (taxable + CGST + SGST + IGST + total)
- Payment reference (if already paid)

## Step 2 — Ledger Mapping

Map each transaction to Tally ledger names. Ask the user for their firm's standard ledger names, or use these defaults:

**Purchase/Expense Ledgers:**
| Category | Default Ledger Name |
|---|---|
| Goods purchase | Purchase A/c (Local) / Purchase A/c (Interstate) |
| Services | Professional Charges / Job Work Charges |
| Freight | Freight Inward |
| Telephone / Internet | Telephone Expenses |
| Electricity | Electricity Charges |
| Rent | Rent Paid |
| Salary | Salaries and Wages |

**GST Ledgers (Input):**
| Tax | Ledger Name |
|---|---|
| CGST Input | CGST Input |
| SGST Input | SGST Input |
| IGST Input | IGST Input |
| Cess Input | Cess Input |

**Party Ledger (Creditors):**
- If vendor exists in Tally: use exact name from Tally
- If new vendor: create as "Sundry Creditors" group, GSTIN set in party details

**Bank/Cash Ledger:**
- Ask: which bank account to use? (e.g. HDFC Current A/c, SBI Current A/c)

## Step 3 — Generate Tally XML

Generate standard Tally voucher XML. Format for a Purchase Voucher:

```xml
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Import Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>[COMPANY NAME]</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Purchase" ACTION="Create">
            <DATE>[YYYYMMDD]</DATE>
            <NARRATION>[Invoice No.] [Vendor Name]</NARRATION>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <PARTYLEDGERNAME>[VENDOR LEDGER]</PARTYLEDGERNAME>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>[PURCHASE LEDGER]</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-[TAXABLE AMOUNT]</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CGST Input</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-[CGST AMOUNT]</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
            <!-- SGST, IGST similarly -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>[VENDOR LEDGER]</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>[TOTAL AMOUNT]</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

Repeat for each voucher. Write the complete XML to `tally_import_[period]_[date].xml`.

## Step 4 — Pre-Import Validation

Before presenting the file, validate:
- [ ] Debit = Credit for each voucher (balanced entry)
- [ ] No voucher has a zero amount
- [ ] All ledger names are in standard Tally format (no special characters that break XML)
- [ ] Dates are in YYYYMMDD format
- [ ] Company name matches exactly

Present a summary:
```
Tally Import File Generated: tally_import_apr2026_20260515.xml

Contents:
  Purchase Vouchers: 47 (Total: Rs.18,42,000)
  Payment Vouchers: 23 (Total: Rs.15,80,000)
  Journal Entries: 3 (TDS adjustments)
  Total Vouchers: 73

Validation: ✓ All entries balanced | ✓ No zero amounts | ✓ XML well-formed

To import: Tally → Gateway → Import Data → Vouchers → select this file
```

## Step 5 — HITL Before Tally Posting

If using the Tally MCP connector (direct posting, not file import), the HITL guardrail in `shared/` will automatically pause and show the verification checklist before any data is posted. You will see:

```
TALLY WRITE — YOUR APPROVAL REQUIRED
Action: Post 73 vouchers | Total Debit: Rs.34,22,000 | Company: [Name]
[ ] Amounts verified  [ ] Ledgers correct  [ ] No duplicates
Approve / Deny
```
