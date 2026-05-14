# Claude for CA

> AI-powered practice assistant for Indian Chartered Accountants — No coding required

Built by **[EurthTech](https://eurth.in)** | Designed by **CogentDeFi** | Mentored by **CA Butchi Babu, Gorantla Associates**

---

## Who Is This For?

Any Indian CA or their team member who wants Claude AI to help with day-to-day practice work:

- Processing invoices and bank statements received by email or as PDF files
- Building and maintaining a Master Accounts workbook in Excel
- Importing transactions into Tally automatically
- Reviewing GST returns before filing and catching ITC mismatches
- Analysing income tax notices and drafting responses
- TDS reconciliation, 26AS mismatch checks, Form 16 generation
- CARO 2020 audit checklists and workpaper drafts
- ROC filing trackers, board resolution drafts

**You do not need to be a software developer.** You can start using these skills with just Claude Desktop — the same app you may already use for general work.

---

## Two Ways to Use This

### Option A — Claude Desktop (Zero Setup, Works Right Now)

**What you need:** [Claude Desktop](https://claude.ai/download) — free download, no subscription needed for basic use.

**How it works in three steps:**

**Step 1.** Download or open any skill file from this repository. Example:
[document-intake/skills/pdf-data-extractor/SKILL.md](document-intake/skills/pdf-data-extractor/SKILL.md)

**Step 2.** Open that file, select all the text, and copy it.

**Step 3.** Open Claude Desktop. Paste the copied text into the chat. Then attach your PDF or describe your task.

That is it. No installation, no terminal, no coding.

**Example conversations you can have:**

> *"I have 23 purchase invoices in this PDF. Extract all of them into a table with: vendor name, GSTIN, invoice number, date, taxable amount, CGST, SGST, IGST, total."*
> → Attach the PDF. Claude returns a structured table you can paste into Excel.

> *"This is my HDFC bank statement for April 2026. The PDF password is PANXXXXXX. Extract all transactions, identify which are vendor payments, and suggest Tally ledger names."*
> → Attach the PDF. Claude reads it, extracts transactions, and maps them to Tally ledger names.

> *"Review this GSTR-3B draft before I file it. Check if the ITC figures match my purchase register and flag any risks."*
> → Paste the GSTR-3B data. Claude analyses and gives a checklist.

---

### Option B — Claude Code (Full Automation, For Tech-Ready Teams)

**What you need:** Claude Code (VS Code extension or terminal). Gives you the complete experience:
- Skills remember your firm profile and client list (offline database — no cloud)
- Every filing action pauses and shows a verification checklist before proceeding
- Compliance calendar monitors alert you to upcoming due dates automatically
- Full audit trail of every AI-assisted action

```bash
git clone https://github.com/eurthtech/claude-for-ca
cd claude-for-ca

# Step 1: Install the core plugin (memory bank + guardrails)
claude install plugin ./shared

# Step 2: One-time onboarding interview (sets up firm profile + client list)
claude install plugin ./cold-start
claude "/cold-start:onboard-firm"

# Step 3: Install the document intake plugin
claude install plugin ./document-intake

# Step 4: Install whichever compliance plugins you need
claude install plugin ./gst-compliance
claude install plugin ./tds-tcs
claude install plugin ./income-tax
```

---

## Document Intake — Process Invoices, Bank Statements & PDFs

This is the most practical feature for daily CA practice work. Here is exactly what it does.

### What You Can Give Claude

| Document Type | What Claude Extracts |
|---|---|
| Purchase invoice PDFs | Vendor name, GSTIN, invoice no., date, line items, CGST/SGST/IGST, total |
| Sales invoice PDFs | Customer name, GSTIN, invoice no., date, taxable value, GST, total |
| Bank statement PDFs | Date, transaction description, debit, credit, balance |
| Credit card statements | Date, merchant name, amount, category |
| Email attachments (via Gmail) | All of the above, fetched directly from your inbox |
| Password-protected PDFs | Same as above — you provide the password, Claude handles the rest |
| Scanned PDFs (image-based) | Same as above — Claude uses vision to read scanned documents |

### What Claude Can Produce From Those Documents

**1. Master Excel Accounts Workbook**

Claude builds or updates a single Excel file with these sheets:

| Sheet | Contents |
|---|---|
| Purchase Register | All vendor invoices — date, vendor, GSTIN, invoice no., amounts, GST breakup |
| Sales Register | All customer invoices |
| Bank Ledger | Bank transactions reconciled to invoices |
| GST Register | CGST/SGST/IGST totals by month — copy-paste ready for GSTR-3B |
| TDS Register | TDS deducted per party per section — ready for 26Q |
| P&L Summary | Month-wise income vs. expenses |
| Balance Sheet | Running assets and liabilities |
| Pending Payables | Invoices received but not yet paid |
| Pending Receivables | Invoices raised but payment not yet received |

**2. Tally Import File (XML or CSV)**

Claude formats the extracted data as a Tally-compatible XML or CSV file. You import it into Tally using Tally's built-in import function (no Tally integration or API needed — just File → Import → Data):

- Each purchase invoice → Purchase Voucher in Tally
- Each payment → Payment Voucher in Tally
- Each bank receipt → Receipt Voucher in Tally
- GST ledgers (CGST/SGST/IGST payable / input) mapped correctly
- TDS entries with correct ledger heads

**3. Exception Report**

Claude also flags:
- Invoices where the vendor GSTIN appears invalid or mismatched
- Invoices where the GST calculation does not foot correctly
- Bank transactions that appear to have no matching invoice
- Duplicate invoice numbers from the same vendor
- Missing invoices (payments made but no corresponding invoice found)

### How to Process a Batch of Invoices (Step by Step)

**Using Claude Desktop (no setup needed):**

1. Collect all invoice PDFs into one folder
2. Open Claude Desktop
3. Copy and paste the skill text from [document-intake/skills/pdf-data-extractor/SKILL.md](document-intake/skills/pdf-data-extractor/SKILL.md)
4. Attach up to 5 PDF files per conversation (Claude Desktop limit per session)
5. Say: *"Extract all invoices. I want: vendor name, GSTIN, invoice number, date, taxable amount, CGST, SGST, IGST, total amount. Give me a table."*
6. Claude returns the table. Copy it into Excel.
7. Repeat for the next batch of files.

For the Master Excel sheet or Tally import, paste the [tally-import-builder](document-intake/skills/tally-import-builder/SKILL.md) skill and provide the table Claude extracted.

**Using Claude Code (automated, handles large batches):**

```
/document-intake:email-invoice-fetch  — fetch this month's invoices from Gmail
/document-intake:pdf-data-extractor   — process a folder of PDF files
/document-intake:master-accounts-sheet — update the Master Excel workbook
/document-intake:tally-import-builder  — generate Tally XML from extracted data
```

---

## All Skills at a Glance

### Document Intake & Accounting

| Skill | What It Does | How to Use |
|---|---|---|
| Email Invoice Fetch | Scans Gmail for emails with invoice or bill attachments and downloads them | `/document-intake:email-invoice-fetch` |
| PDF Data Extractor | Reads any PDF (including password-protected or scanned) and extracts structured data | `/document-intake:pdf-data-extractor` |
| Bank Statement Processor | Extracts all transactions from a bank or credit card statement PDF | `/document-intake:bank-statement-processor` |
| Master Accounts Sheet | Builds or updates the Master Excel workbook with all registers | `/document-intake:master-accounts-sheet` |
| Tally Import Builder | Formats extracted data as Tally-ready XML or CSV for direct import | `/document-intake:tally-import-builder` |

### GST Compliance

| Skill | What It Does |
|---|---|
| GSTR-3B Review | Checks your GSTR-3B draft — ITC eligibility, cash balance, reversals |
| GSTR-2B Reconciliation | Compares your purchase register with GSTR-2B — flags mismatches |
| GST Notice Triage | Reads a GST notice, explains the demand, suggests the response |
| GSTR-9 / 9C Review | Annual return cross-check and reconciliation with books |

### Income Tax

| Skill | What It Does |
|---|---|
| ITR Review | Cross-checks ITR figures with Form 26AS and AIS before filing |
| AO Notice Analysis | Explains an Assessing Officer notice in plain language, suggests reply |
| Advance Tax Tracker | Calculates quarterly advance tax installments and flags shortfalls |

### TDS / TCS

| Skill | What It Does |
|---|---|
| TDS Default Detector | Finds late deductions, short deductions, and non-deduction cases |
| 26AS Reconciliation | Compares TDS per books with 26AS credits |
| Form 16 Generator | Prepares Form 16 / 16A data from TDS records |

### Audit & Assurance

| Skill | What It Does |
|---|---|
| CARO 2020 Checklist | Goes through all CARO 2020 reporting clauses interactively |
| Audit Risk Matrix | Builds an inherent + control risk matrix for a client |
| Workpaper Drafter | Drafts SA-compliant audit workpapers |

---

## Safety: You Always Approve Before Claude Acts

Claude will **never automatically file** any return, modify Tally data, or send any communication without showing you a detailed checklist and waiting for your explicit approval.

**Before any GST filing, you see:**
```
GST FILING — YOUR APPROVAL REQUIRED

Return    : GSTR-3B
Client    : Gorantla Associates
GSTIN     : 37XXXXX1234Z5
Period    : April 2026
Tax Amount: Rs.2,34,500

Before approving, confirm:
  [ ] GSTR-1 is filed for this period
  [ ] ITC reconciled with GSTR-2B
  [ ] Cash ledger balance is sufficient
  [ ] Client has authorised this filing

Approve = proceed  |  Deny = stop
```

**Before any Tally write:**
```
TALLY WRITE — YOUR APPROVAL REQUIRED
⚠  This action modifies accounting data and is not easily reversible.

Action       : Create 47 Purchase Vouchers
Company      : Gorantla Infra Pvt Ltd
Total Debit  : Rs.18,42,000
Date Range   : 01 Apr 2026 to 30 Apr 2026

  [ ] Voucher amounts are correct
  [ ] Ledger heads are correctly mapped
  [ ] No duplicate entries

Approve = post to Tally  |  Deny = stop
```

The same checklist pattern applies to TDS returns, ITR submissions, and MCA filings.

All AI-assisted actions are saved in a **local audit log** — readable at any time.

---

## Your Data Stays Local

- All client data, firm profile, compliance calendar, and audit trail are stored in a **local SQLite database** on your own machine
- No cloud sync, no third-party data storage
- When using Claude Desktop without connectors, files you attach are processed within your Claude session only
- Password-protected PDFs: you provide the password in the chat, it is used to open the file and is not stored

---

## Frequently Asked Questions

**Can I use this with only the free Claude plan?**
Yes. You can copy any SKILL.md file and paste it into Claude to use it. The automatic memory, compliance calendar, and monitoring features require Claude Code.

**Do I need to install anything?**
For Option A (Claude Desktop): nothing to install. Download Claude Desktop, paste a skill, and start working.
For Option B (Claude Code): you need Claude Code and to run `git clone` once.

**Can Claude file GST returns or TDS returns on its own?**
No. Claude will never auto-file. Every filing action is blocked until you approve it with a checklist. This is built into the system and cannot be bypassed.

**What if my PDF is in Telugu or Hindi?**
Claude reads multilingual PDFs. For Tally output and Excel, it normalises to English.

**What accounting software does this support?**
Primarily Tally ERP (via XML or CSV import). The Master Excel output works with any spreadsheet application. Zoho Books and QuickBooks import formats are on the roadmap.

**Is this affiliated with Anthropic or the ICAI?**
No. This is an independent open-source project built by EurthTech. It uses Anthropic's Claude API but is not endorsed by Anthropic or the Institute of Chartered Accountants of India.

---

## Credits

Built by **EurthTech** | Designed with **CogentDeFi** | Mentored by **CA Butchi Babu, Gorantla Associates**

Inspired by the `claude-for-legal` reference architecture by Anthropic.

---

## License

Apache 2.0 — free to use, modify, and deploy. Attribution appreciated.
