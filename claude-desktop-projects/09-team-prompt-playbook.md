# Team Prompt Playbook
## Gorantla Associates — Standard Prompts for Daily CA Work
### Version 1.0 | For use with Claude Desktop → "CA Team Workspace" project

---

## HOW TO USE THIS PLAYBOOK

1. Find the task you need (use Ctrl+F to search)
2. Copy the prompt inside the `--- COPY FROM HERE ---` block
3. Replace everything in `[SQUARE BRACKETS]` with the actual information
4. Paste raw documents / data below the prompt (just paste the text from invoices, statements, etc.)
5. Send to Claude — get your output

**Tip for interns**: You don't need to understand the whole prompt. Just copy it, fill in the blanks, and paste your document below.

---

# SECTION A — DOCUMENT & INVOICE PROCESSING

---

## A1 — Extract Invoice Data (Single Invoice → Excel Row)

**Use when**: You have one invoice/bill and need to enter it into the Purchase Register or any Excel register.

**What to provide**: Paste the full text of the invoice (from PDF, email, or type it out)

```
--- COPY FROM HERE ---
Extract all data from the invoice below and give me one row in a table.

Use EXACTLY these columns:
| Date | Vendor Name | Vendor GSTIN | Invoice Number | Invoice Date | Description of Goods/Services | HSN/SAC Code | Taxable Amount (Rs.) | CGST Rate % | CGST Amount (Rs.) | SGST Rate % | SGST Amount (Rs.) | IGST Rate % | IGST Amount (Rs.) | Total Invoice Amount (Rs.) | Payment Terms |

Rules:
- If any field is not on the invoice, write "Not mentioned"
- Amounts in numbers only, no commas or Rs. symbol in cells
- Date format: DD-MM-YYYY
- If IGST is used (interstate), leave CGST and SGST blank and vice versa

[PASTE INVOICE TEXT BELOW THIS LINE]

--- END COPY ---
```

**Expected output**: One table row ready to copy-paste into Excel Purchase Register.

---

## A2 — Extract Multiple Invoices (Batch → Excel Table)

**Use when**: You have 5–30 invoices to enter at once (paste all of them one after another).

```
--- COPY FROM HERE ---
I am pasting multiple invoices below. Extract data from ALL of them and give me a complete table.

Use EXACTLY these columns:
| Sr. No. | Date | Vendor Name | Vendor GSTIN | Invoice Number | Invoice Date | Description | HSN/SAC | Taxable Amount | CGST % | CGST Amount | SGST % | SGST Amount | IGST % | IGST Amount | Total Amount |

Rules:
- One row per invoice
- Date format: DD-MM-YYYY
- Numbers only in amount columns (no Rs., no commas)
- If any field missing from invoice: write "NK" (Not Known)
- At the end, give me TOTALS row for all amount columns

[PASTE ALL INVOICES BELOW — ONE AFTER ANOTHER]

--- END COPY ---
```

---

## A3 — Extract Sales Invoice Data

**Use when**: Client has given you their sales invoices to compile.

```
--- COPY FROM HERE ---
Extract all data from the sales invoice(s) below and give me a table.

Use EXACTLY these columns:
| Sr. No. | Invoice Date | Invoice Number | Customer Name | Customer GSTIN | State of Supply | Place of Supply | Description | HSN/SAC | Qty | Unit | Rate | Taxable Amount | CGST % | CGST Amount | SGST % | SGST Amount | IGST % | IGST Amount | Total Amount | Whether RCM Applicable |

Rules:
- Date format: DD-MM-YYYY
- Numbers only in amount columns
- For B2C (no GSTIN of customer): write "B2C" in Customer GSTIN column
- Give TOTALS row at the end

[PASTE SALES INVOICES BELOW]

--- END COPY ---
```

---

## A4 — Extract Payment / Receipt from Bank Statement

**Use when**: You have a bank statement (pasted text) and need to categorise transactions for ledger posting.

```
--- COPY FROM HERE ---
I am pasting a bank statement below. Extract all transactions and give me a table.

Use EXACTLY these columns:
| Sr. No. | Transaction Date | Value Date | Description (from bank) | Cheque/Ref No. | Debit Amount | Credit Amount | Balance | Likely Ledger Head | Remarks |

For "Likely Ledger Head" — use your knowledge of typical CA firm client transactions to suggest the most likely account head (e.g. "Salary", "Office Rent", "GST Payment", "Loan Repayment", "Sales Receipt", "Supplier Payment", etc.)

Rows where you are uncertain about the ledger head — mark Remarks as "Please verify"

[PASTE BANK STATEMENT TEXT BELOW]

--- END COPY ---
```

---

## A5 — Summarise a Contract or Agreement

**Use when**: Client has shared a contract and you need a quick summary for CA review.

```
--- COPY FROM HERE ---
Summarise the contract/agreement pasted below. Give me:

1. PARTIES INVOLVED — Names and roles (buyer/seller/service provider/lender etc.)
2. KEY DATES — Agreement date, start date, end date, renewal date
3. FINANCIAL TERMS — Amount, payment schedule, penalties, security deposit
4. GST IMPLICATIONS — Is GST applicable? What rate? Who charges it?
5. TDS IMPLICATIONS — Is TDS applicable? Under which section? Rate?
6. KEY OBLIGATIONS — What each party must do (2-3 bullet points each)
7. TERMINATION CLAUSES — How can the contract be ended?
8. ⚠️ FLAGS FOR CA REVIEW — Any unusual terms, high-value obligations, or compliance risks

Keep the summary concise. Use bullet points.

[PASTE CONTRACT TEXT BELOW]

--- END COPY ---
```

---

## A6 — Extract Data from Salary Slip / Payslip

**Use when**: You need to enter salary data into payroll register.

```
--- COPY FROM HERE ---
Extract payroll data from the salary slip(s) below and give me a table.

Use EXACTLY these columns:
| Employee Name | Employee ID | Designation | Month | Basic Salary | DA | HRA | Special Allowance | Other Allowances | Gross Salary | PF Employee (12%) | ESIC Employee (0.75%) | Professional Tax | TDS (194B/192) | Other Deductions | Net Pay | PF Employer (12%) | ESIC Employer (3.25%) |

Numbers only. If any field not in slip: write 0.

[PASTE SALARY SLIP TEXT(S) BELOW]

--- END COPY ---
```

---

# SECTION B — EXCEL DATA PREPARATION

---

## B1 — Prepare Expense Register from Petty Cash / Vouchers

**Use when**: Client has given you a list of petty cash expenses (verbally, in a note, or from photos of vouchers).

```
--- COPY FROM HERE ---
Organise the expenses listed below into a proper expense register table.

Use EXACTLY these columns:
| Sr. No. | Date | Voucher No. | Description | Paid To | Amount (Rs.) | Expense Head | GST Applicable (Y/N) | If Yes — Taxable Amount | GST Amount | Invoice Available (Y/N) | Remarks |

For "Expense Head" — use standard heads: Office Supplies / Travelling / Postage & Courier / Printing & Stationery / Electricity / Telephone / Repair & Maintenance / Miscellaneous

Sort by Date.

[PASTE EXPENSE LIST BELOW]

--- END COPY ---
```

---

## B2 — Prepare TDS Working Sheet

**Use when**: You have a list of payments made and need to check TDS applicability and calculate amounts.

```
--- COPY FROM HERE ---
For each payment listed below, check TDS applicability and prepare a TDS working table.

Use EXACTLY these columns:
| Sr. No. | Payment Date | Payee Name | Payee PAN | Nature of Payment | Amount Paid (Rs.) | TDS Section | TDS Rate % | TDS Amount (Rs.) | Due Date to Deposit TDS | Remarks |

Rules:
- For each payment, identify the correct TDS section (e.g. 194C for contractors, 194J for professionals, 194I for rent, 192 for salary)
- If payee PAN not provided: calculate TDS at 20% (higher rate for no PAN)
- TDS deposit due: 7th of following month (for March: 30 April)
- If no TDS applicable: write "Not applicable" in TDS section and 0 in amount

[LIST PAYMENTS BELOW — FORMAT: Date | Payee | Nature | Amount | PAN (if available)]

--- END COPY ---
```

---

## B3 — Prepare GST Summary from Sales/Purchase Figures

**Use when**: You have monthly totals and need to prepare GSTR-3B working.

```
--- COPY FROM HERE ---
Prepare a GSTR-3B summary working based on the figures given below.

Give me a table with:
1. OUTWARD SUPPLIES (Sales)
   | Category | Taxable Value | CGST | SGST | IGST | Total |
   Categories: B2B (registered buyers) | B2C Large (>2.5L interstate) | B2C Small | Nil rated/Exempt | Zero rated (export)

2. INWARD SUPPLIES — ITC AVAILABLE
   | Source | Taxable Value | IGST | CGST | SGST | Total ITC |
   Sources: From suppliers (GSTR-2B) | Import of goods | Import of services | Inward RCM supplies

3. TAX PAYABLE CALCULATION
   | | CGST | SGST | IGST |
   | Output tax liability | | | |
   | Less: ITC from CGST | | | |
   | Less: ITC from SGST | | | |
   | Less: ITC from IGST | | | |
   | Net tax payable in cash | | | |

4. ⚠️ FLAGS — Any ITC that may be blocked u/s 17(5): personal use, food, club, motor vehicles etc.

Note: This is working paper only. CA must review before filing.

[PROVIDE FIGURES BELOW]

--- END COPY ---
```

---

## B4 — Prepare Income Tax Computation Sheet

**Use when**: You have client's income details and need to prepare basic tax computation.

```
--- COPY FROM HERE ---
Prepare an income tax computation for the taxpayer details given below.

Format it as a proper computation sheet:

INCOME COMPUTATION — AY [FILL: 2025-26 or 2026-27]
Name: [NAME]
PAN: [PAN]

| Head of Income | Particulars | Amount (Rs.) |
|----------------|-------------|-------------|
| Salary | Gross salary | |
| | Less: Standard deduction (50,000) | |
| | Net salary income | |
| House Property | Annual letable value | |
| | Less: Municipal taxes | |
| | Less: 30% deduction (Sec 24a) | |
| | Less: Interest on home loan (Sec 24b) | |
| | Net house property income | |
| Capital Gains | STCG | |
| | LTCG | |
| Other Sources | Interest, dividends etc. | |
| **GROSS TOTAL INCOME** | | |
| Less: Chapter VI-A deductions | 80C (max 1,50,000) | |
| | 80D medical insurance | |
| | 80E education loan interest | |
| | Other deductions | |
| **NET TAXABLE INCOME** | | |

TAX CALCULATION:
Show under BOTH old and new regime.
Identify which regime is more beneficial.

[PROVIDE CLIENT INCOME DETAILS BELOW]

--- END COPY ---
```

---

# SECTION C — CLIENT EMAILS AND LETTERS

---

## C1 — Request Documents from Client

**Use when**: You need to request pending documents from a client.

```
--- COPY FROM HERE ---
Draft a formal email requesting documents from a client. Use professional Indian English, CA firm letterhead tone.

Details:
- Client Name: [CLIENT NAME / COMPANY NAME]
- Our Firm: Gorantla Associates
- Purpose of documents: [e.g. GST return filing / Income Tax Return / Audit / TDS filing]
- Period: [e.g. April 2025 to March 2026 / Q1 FY 2025-26]
- Documents needed: [LIST EACH DOCUMENT]
- Deadline to receive by: [DATE]
- Any previous reminder sent: [Yes/No — if Yes, mention how many times]

Make the tone: professional but friendly. Not too harsh. Mention the compliance deadline and that we need to file on time.

--- END COPY ---
```

---

## C2 — Compliance Deadline Reminder to Client

**Use when**: Reminding client that a compliance deadline is approaching.

```
--- COPY FROM HERE ---
Draft a formal compliance reminder email/letter for our client.

Details:
- Client Name: [CLIENT NAME]
- Compliance Type: [e.g. GSTR-1 filing / TDS return / Advance tax / ROC filing]
- Due Date: [DATE]
- What is needed from the client: [e.g. invoice data / payment of tax / approval to file]
- Late fee/penalty if missed: [mention the amount or say "heavy late fees apply"]
- Urgency: [e.g. 3 days left / 1 week left]

Tone: Urgent but professional. Clearly explain what happens if deadline is missed.

--- END COPY ---
```

---

## C3 — Reply to Client Query (Tax / Compliance Question)

**Use when**: Client has asked a question and you need to send a clear, professional reply.

```
--- COPY FROM HERE ---
Draft a professional reply to a client's query.

Client's question / query:
[PASTE OR DESCRIBE THE CLIENT'S QUESTION HERE]

Key points to include in the reply:
[LIST 2-3 POINTS you want covered — e.g. "explain Section 44AD", "mention turnover limit", "advise to consult CA before deciding"]

Firm: Gorantla Associates
Tone: Formal, helpful, easy to understand (client may not know accounting terms)
End the email with: "For further queries or to discuss, please contact our office."

Note: Add a disclaimer at the end: "This reply is for general guidance only and does not constitute professional advice. Please consult CA Butchi Babu before taking any action."

--- END COPY ---
```

---

## C4 — Fee Reminder (First Reminder)

```
--- COPY FROM HERE ---
Draft a polite first reminder for outstanding fees.

Details:
- Client Name: [CLIENT NAME]
- Outstanding Amount: Rs. [AMOUNT]
- Invoice Date: [DATE]
- Services for which fee is due: [e.g. GST filing April-June / Annual audit FY 2024-25]
- Payment details to mention: [Bank name, account number — or say "as per earlier communication"]

Tone: Polite, professional, friendly. Assume it may be an oversight. No pressure yet.

--- END COPY ---
```

---

## C5 — Fee Reminder (Second / Final Reminder)

```
--- COPY FROM HERE ---
Draft a firm but professional second/final fee reminder.

Details:
- Client Name: [CLIENT NAME]
- Outstanding Amount: Rs. [AMOUNT]
- Due Since: [DATE / NUMBER OF MONTHS]
- Previous Reminders Sent: [NUMBER]
- Consequence of non-payment: [e.g. "we may need to pause work on pending filings"]

Tone: Firm. Professional. Make clear this is the final reminder before escalation. But not rude or threatening.

--- END COPY ---
```

---

## C6 — Reply to a GST / Income Tax Notice

**Use when**: Client has received a tax notice and you need to draft a preliminary reply.

```
--- COPY FROM HERE ---
Draft a formal reply to the following tax notice. This is a preliminary draft for CA review.

Notice Details:
- Notice Type / Section: [e.g. DRC-01 u/s 73 / 143(2) / 148]
- Issued by: [GST department / Income Tax department / GST officer name if mentioned]
- Notice Date: [DATE]
- Reference / DIN Number: [NUMBER]
- Demand or Issue Raised: [DESCRIBE WHAT THE NOTICE SAYS]
- Client's Position / Facts: [DESCRIBE THE CLIENT'S SIDE — what actually happened]
- Supporting Documents Available: [LIST]

Draft a professional reply that:
1. Acknowledges the notice with reference number
2. States the facts clearly on behalf of the client
3. Provides the explanation / justification
4. Lists supporting documents being submitted
5. Requests time extension if needed (mention if yes)

End with: "This is a draft only. Final reply must be reviewed and signed by CA Butchi Babu before submission."

--- END COPY ---
```

---

# SECTION D — ACCOUNTS AND LEDGER REVIEW

---

## D1 — Ledger Analysis (Find Unusual Entries)

**Use when**: You have exported a ledger and want to check for anything unusual or incorrect.

```
--- COPY FROM HERE ---
Analyse the ledger data pasted below. Identify:

1. ⚠️ UNUSUAL ENTRIES — Any entry that seems inconsistent (e.g. credit in normally debit-only accounts, round numbers, entries on holidays, unusually large amounts compared to others)
2. MISSING ENTRIES — Any expected regular entries that seem absent (e.g. monthly rent not appearing in one month)
3. POTENTIAL ERRORS — Any entries where the amount or account head seems wrong
4. DUPLICATE ENTRIES — Any entries that look like possible duplicates
5. SUMMARY — Total debits, total credits, closing balance, net movement for the period

Output as:
- First: Clean summary table
- Then: Flagged entries table with column "Reason for Flag"
- Finally: 3-5 bullet point overall observations

[PASTE LEDGER DATA BELOW — can be exported from Tally as text]

--- END COPY ---
```

---

## D2 — Accounts Payable Ageing

**Use when**: You have a list of outstanding creditor balances and want ageing analysis.

```
--- COPY FROM HERE ---
Prepare an accounts payable ageing analysis from the data below.

Ageing buckets:
| Creditor Name | Total Outstanding | Current (0-30 days) | 31-60 days | 61-90 days | 91-180 days | >180 days | Oldest Invoice Date | ⚠️ MSME Flag |

For "⚠️ MSME Flag": Mark "CHECK" for any creditor where the balance is outstanding more than 45 days (possible MSME payment rule violation under Section 43B(h))

Sort by: Total Outstanding descending.

Give TOTAL row at the bottom.

[PASTE CREDITOR LIST / AGEING DATA BELOW]

--- END COPY ---
```

---

## D3 — Bank Reconciliation

**Use when**: You have bank statement and cash book and need to prepare BRS.

```
--- COPY FROM HERE ---
Prepare a Bank Reconciliation Statement (BRS) as at [DATE].

I will provide:
A) Bank balance as per Cash Book
B) Bank balance as per Bank Statement
C) List of unreconciled items

Format the BRS as:

BANK RECONCILIATION STATEMENT
As at: [DATE]
Bank Account: [BANK NAME and ACCOUNT NUMBER]

Balance as per Cash Book: Rs. ___
Add: Cheques issued but not presented: [list with amounts]
Less: Deposits in transit (recorded in books, not yet in bank): [list]
Add: Credits in bank not in books (bank charges reversed, interest received etc.): [list]
Less: Debits in bank not in books (bank charges, ECS payments etc.): [list]
Balance as per Bank Statement: Rs. ___

The two balances should agree. If they don't — highlight the difference and suggest what may be missing.

[PROVIDE FIGURES AND ITEMS BELOW]

--- END COPY ---
```

---

## D4 — Monthly MIS Report from Trial Balance

**Use when**: You have a trial balance (exported from Tally) and need to prepare a monthly summary report for the client.

```
--- COPY FROM HERE ---
Prepare a management summary (MIS) report from the trial balance data below.

Structure the report as:

MONTHLY MIS REPORT — [MONTH YEAR]
Company: [COMPANY NAME]

1. PROFIT & LOSS SUMMARY
   | | Current Month | YTD | Same Month Last Year |
   | Revenue | | | |
   | Cost of Goods Sold | | | |
   | Gross Profit | | | |
   | Gross Margin % | | | |
   | Operating Expenses | | | |
   | EBITDA | | | |
   | Finance Cost | | | |
   | Net Profit Before Tax | | | |

2. KEY RATIOS (calculate from available data)
   - Gross Margin %
   - Operating Margin %
   - Debtor Days (if debtor balance and sales given)
   - Creditor Days (if creditor balance and purchases given)

3. TOP 3 EXPENSE CATEGORIES (by amount)

4. ⚠️ FLAGS FOR REVIEW — Any item that looks unusual vs prior months or that needs CA attention

[PASTE TRIAL BALANCE DATA BELOW]

--- END COPY ---
```

---

# SECTION E — COMPLIANCE CHECKLISTS AND VERIFICATION

---

## E1 — Monthly Compliance Due Dates (Current Month)

**Use when**: Beginning of each month — get all due dates for the month.

```
--- COPY FROM HERE ---
Give me a complete compliance calendar for the month of [MONTH] [YEAR] for an Indian CA firm.

Include ALL due dates for:
- GST filings (GSTR-1, GSTR-3B, GSTR-9 if applicable, CMP-08, IFF)
- Income Tax (advance tax, TDS deposit, TDS returns, ITR deadlines)
- TDS return filing (24Q/26Q/27Q/27EQ)
- MCA/ROC filings (DPT-3, MSME-1, BEN-2, DIR-3 KYC if applicable)
- Payroll (PF deposit, ESIC deposit, PT)
- Other statutory due dates

Format as:
| Due Date | Compliance | Form | Applicable To | Penalty for Delay |

Sort by date.
Highlight dates within the NEXT 7 DAYS in bold.

--- END COPY ---
```

---

## E2 — GST Invoice Compliance Check

**Use when**: Client has given you a batch of invoices and you need to verify GST compliance before filing.

```
--- COPY FROM HERE ---
Check the following invoices for GST compliance. For each invoice, verify:

Checklist items:
1. GSTIN of supplier — correct format (15 characters, starts with state code)?
2. Invoice number — sequential and valid?
3. Date — within the current financial year?
4. HSN/SAC code — mentioned? Appropriate for the goods/services?
5. Tax rate — correct rate for the HSN/SAC?
6. CGST + SGST vs IGST — correctly used (IGST for interstate, CGST+SGST for intrastate)?
7. Calculation — taxable amount × rate = tax amount correct?
8. Total — taxable + taxes = invoice total correct?
9. Place of supply — mentioned?

Output as:
| Invoice No. | Date | Vendor | ✅ OK or ❌ Issue | Issues Found |

Summary at end: Total invoices checked / Total OK / Total with issues

[PASTE INVOICE DATA BELOW]

--- END COPY ---
```

---

## E3 — 26AS / AIS Reconciliation

**Use when**: You have 26AS data and need to reconcile with books.

```
--- COPY FROM HERE ---
Reconcile the TDS/TCS data from 26AS with the figures I provide from books of accounts.

26AS data:
[PASTE 26AS DATA - Deductor name, TAN, Amount deducted, Amount deposited]

Books data:
[PASTE TDS RECEIVABLE LEDGER FROM BOOKS]

Prepare a reconciliation table:
| Deductor Name | TAN | Amount in 26AS | Amount in Books | Difference | Possible Reason for Difference | Action Required |

Categorise differences as:
- ✅ MATCH — No action
- ⚠️ IN 26AS, NOT IN BOOKS — Add to books
- ⚠️ IN BOOKS, NOT IN 26AS — Contact deductor; may not have deposited
- ❌ AMOUNT MISMATCH — Get corrected certificate

Give total of all differences at the bottom.

--- END COPY ---
```

---

# SECTION F — REPORTS AND SUMMARIES

---

## F1 — Client Status Report (Weekly)

**Use when**: Preparing a weekly status update for CA partner on pending client work.

```
--- COPY FROM HERE ---
Prepare a weekly client status report from the information below.

Format as:
| Client Name | Work Type | Status | Pending Since | Documents Pending From Client | Action Required | Priority |

Priority levels: 🔴 Urgent (deadline < 3 days) / 🟡 This week / 🟢 Okay

Also give:
- Count of urgent items
- Count of items where documents are awaited from client (vs items where our work is pending)
- Any compliance deadline this week that is at risk

[PROVIDE CLIENT WORK STATUS BELOW — one client per line is fine]

--- END COPY ---
```

---

## F2 — Meeting Notes → Action Items

**Use when**: After a client meeting, you have notes and need to convert to action items.

```
--- COPY FROM HERE ---
Convert the following meeting notes into a structured action item list.

Format as:
| Sr. No. | Action Item | Owner (Client / Our Firm / CA Partner) | Deadline | Priority | Notes |

Also prepare:
- 2-paragraph meeting summary (what was discussed and decided)
- 3 key decisions made in the meeting

[PASTE MEETING NOTES BELOW — even rough handwritten-style notes are fine]

--- END COPY ---
```

---

## F3 — Prepare a File Note

**Use when**: Something important happened with a client (notice received, unusual transaction, client instruction given) and you need to document it formally.

```
--- COPY FROM HERE ---
Draft a formal File Note for our records.

Details:
- Client: [CLIENT NAME]
- Date of event: [DATE]
- Type of event: [e.g. GST notice received / client gave verbal instruction / unusual payment found]
- What happened: [DESCRIBE IN YOUR OWN WORDS — doesn't need to be formal]
- What action was taken / to be taken: [LIST ACTIONS]
- By whom: [Staff name]
- CA partner to be informed: Yes / No

Format as a proper File Note with:
- Date
- File Note Number: FN/[YEAR]/[SEQUENTIAL NUMBER — leave blank for now]
- Subject
- Body (formal narration)
- Prepared by / Reviewed by fields (leave blank)

--- END COPY ---
```

---

# SECTION G — CALCULATIONS

---

## G1 — GST Late Fee Calculation

```
--- COPY FROM HERE ---
Calculate GST late fee for the following situation:

Return Type: [GSTR-1 / GSTR-3B / GSTR-9 / other]
Taxpayer Category: [Regular / Composition / nil return]
Due Date: [DD-MM-YYYY]
Date of Filing: [DD-MM-YYYY or "not yet filed"]
Turnover (if annual return): Rs. [AMOUNT]
Is this a nil return: [Yes / No]

Calculate:
1. Number of days late
2. Late fee per day (CGST + SGST separately)
3. Total late fee
4. Whether any waiver scheme applies (mention if government has announced amnesty)
5. Interest u/s 50 if applicable (18% p.a. on tax payable — only for GSTR-3B)

Show working clearly.

--- END COPY ---
```

---

## G2 — TDS Default Interest Calculation (Section 201(1A))

```
--- COPY FROM HERE ---
Calculate TDS default interest u/s 201(1A) for the following:

Nature of default: [Late deduction / Late deposit / Non-deduction]
Date on which amount was paid/credited to payee: [DATE]
Date on which TDS was deducted: [DATE or "not deducted"]
Date on which TDS was deposited: [DATE or "not deposited"]
TDS amount: Rs. [AMOUNT]

Calculate:
1. Interest @ 1% per month from date of deductibility to date of deduction
2. Interest @ 1.5% per month from date of deduction to date of deposit
3. Total interest
4. 234E late fee if quarterly return is delayed (Rs.200/day, max = TDS amount)

Note: Months are counted as part months (even 1 day = 1 month).
Show date-wise working.

--- END COPY ---
```

---

## G3 — PF and ESIC Calculation

```
--- COPY FROM HERE ---
Calculate PF and ESIC contributions for the following employees:

[PASTE EMPLOYEE LIST: Name | Basic+DA salary | Gross Salary]

For each employee calculate:
| Employee Name | Basic+DA | Gross Salary | PF Employee 12% | PF Employer (EPF 3.67%) | EPS (8.33% capped at Rs.1250) | EDLI (0.5% capped Rs.75) | ESIC Applicable (Y/N) | ESIC Employee 0.75% | ESIC Employer 3.25% |

Rules:
- PF: Based on Basic+DA (or actual if LOP)
- PF ceiling: No ceiling for contribution; EPS capped at Rs.15,000 basic (max EPS = Rs.1,250)
- ESIC: Only if gross salary ≤ Rs.21,000
- If gross > Rs.21,000: Mark ESIC as N/A

Give totals row at the bottom.

--- END COPY ---
```

---

## G4 — Professional Tax Calculation (Multi-State)

```
--- COPY FROM HERE ---
Calculate Professional Tax for the following employees. 

State: [KARNATAKA / MAHARASHTRA / TELANGANA / ANDHRA PRADESH / TAMIL NADU / WEST BENGAL]

[PASTE EMPLOYEE LIST: Name | Gross Monthly Salary]

Give me:
| Employee Name | Gross Salary | PT Applicable (Y/N) | PT Amount (Rs.) |

Also mention: PT deposit due date and authority to pay PT to in [STATE].

--- END COPY ---
```

---

# SECTION H — QUICK REFERENCE CHECKS

---

## H1 — Which ITR Form to Use?

```
--- COPY FROM HERE ---
Tell me which ITR form a taxpayer should use.

Taxpayer details:
- Type: [Individual / HUF / Firm / Company / LLP / Trust]
- Income sources: [LIST ALL — e.g. salary, house property, capital gains, business, interest, dividends, foreign income]
- Turnover (if business): Rs. [AMOUNT]
- Opting for presumptive taxation (44AD/44ADA): [Yes / No / Not sure]
- Director in any company: [Yes / No]
- Foreign assets or income: [Yes / No]
- Agricultural income: Rs. [AMOUNT]

Give:
1. Recommended ITR form with reason
2. Any conditions to watch out for
3. Due date for filing

--- END COPY ---
```

---

## H2 — TDS Rate Check

```
--- COPY FROM HERE ---
Check TDS applicability and rate for the following payment:

Nature of payment: [DESCRIBE — e.g. "consulting fee to advocate firm", "rent for office space", "purchase of goods from manufacturer"]
Amount of this payment: Rs. [AMOUNT]
Total payments to this party in the financial year so far: Rs. [AMOUNT]
Type of payee: [Individual / Firm / LLP / Company / HUF]
Is payee an MSME: [Yes / No / Not known]
Has payee submitted lower deduction certificate (Form 13): [Yes — rate _% / No]
Is payee's PAN available: [Yes / No]

Tell me:
1. TDS section applicable
2. Threshold limit
3. TDS rate
4. TDS amount on this payment
5. Due date to deposit
6. Any exceptions or special situations to note

--- END COPY ---
```

---

## H3 — GST Rate Check for a Product or Service

```
--- COPY FROM HERE ---
Check GST rate and HSN/SAC code for the following:

Item / Service description: [DESCRIBE IN DETAIL — e.g. "ready-made garments sold below Rs.1000", "software development services", "rice husking mill services"]
Business context: [What does the client do? e.g. trader / manufacturer / service provider]
State of customer (for place of supply): [STATE NAME]

Tell me:
1. HSN code (for goods) or SAC code (for services)
2. GST rate (CGST + SGST or IGST)
3. Whether IGST or CGST+SGST applies for this transaction
4. Any exemption available
5. Any special conditions (e.g. reverse charge, e-invoicing, composition restriction)

--- END COPY ---
```

---

## END OF PLAYBOOK

**Total prompts in this playbook**: 30

**How to request a new prompt**: Tell CA Butchi Babu or the senior in charge what task you need a standard prompt for. We will add it to the next version.

**Version history**:
- v1.0 (May 2026): Initial release — 30 prompts across 8 sections
