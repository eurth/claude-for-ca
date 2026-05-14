# Claude for CA

> AI-powered practice assistant for Indian Chartered Accountants

**Built by [EurthTech](https://eurth.in) · Designed by CogentDeFi · Mentored by CA Butchi Babu, Gorantla Associates**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Public Repository](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](#contributing)

---

## What Is This?

A complete AI assistant toolkit for Indian CA firms — covering GST, Income Tax, TDS, Audit, MCA, Payroll, and daily practice management.

**You do not need to be a software developer to use this.** The primary use is through [Claude Desktop](https://claude.ai/download) — a free app on your computer. You chat with Claude in plain English and get professional CA-quality outputs.

This repository was built for and with **CA Butchi Babu's team at Gorantla Associates** and is now open to the entire CA community.

---

## ⚡ Start Here — Get Running in 30 Minutes (No Technical Skills Needed)

### Step 1 — Download Claude Desktop
Go to **[claude.ai/download](https://claude.ai/download)** → Download for Windows or Mac → Install like any normal app → Log in with a Claude account ([claude.ai](https://claude.ai) — free or Pro plan).

### Step 2 — Create Your First Project
In Claude Desktop: Click **"+ New Project"** → give it a name (e.g. **GST Compliance**) → click **"Set project instructions"**.

Open the file [`claude-desktop-projects/01-gst-compliance.md`](claude-desktop-projects/01-gst-compliance.md) from this repository (you can view it directly on GitHub). Copy the text between the `━━━` separator lines and paste it into the instructions box → Save.

### Step 3 — Start Working
Type your question in plain English. Examples:

> *"My client received a DRC-01 notice for Rs.2.8 lakh ITC mismatch in GSTR-3B for FY 2023-24. Help me analyse and draft a reply."*

> *"Calculate GSTR-3B for April 2026 — taxable outward supplies Rs.18,50,000 at 18%, ITC available Rs.2,10,000."*

> *"What is the late fee for GSTR-1 filed 45 days after due date? Turnover Rs.3.5 Cr, not a nil return."*

That is it. No terminal, no code, no installation beyond Claude Desktop.

→ **[Full setup guide with screenshots: `claude-desktop-projects/00-SETUP-GUIDE.md`](claude-desktop-projects/00-SETUP-GUIDE.md)**

---

## 📋 Team Prompt Playbook — For Daily Office Use

If you have junior staff or interns, the **[Team Prompt Playbook](claude-desktop-projects/09-team-prompt-playbook.md)** solves a common problem: *team members don't know how to write good prompts and get inconsistent results.*

The playbook has **30 ready-to-use prompts** for every common CA office task. Each prompt has `[PLACEHOLDERS]` to fill in — no prompting skill required.

| Section | Prompts |
|---------|---------|
| Document & Invoice Processing | Extract invoices to Excel, bank statements, contracts, payslips |
| Excel Data Preparation | GSTR-3B working, TDS working, IT computation, expense register |
| Client Emails & Letters | Document requests, deadline reminders, fee reminders, notice replies |
| Accounts & Ledger Review | Ledger anomaly detection, AP ageing, bank reconciliation, MIS report |
| Compliance Checklists | Monthly due dates, GST invoice compliance check, 26AS reconciliation |
| Calculations | GST late fee, TDS interest (201(1A)), PF/ESIC, Professional Tax |
| Quick Reference | ITR form selector, TDS rate check, GST rate / HSN-SAC lookup |

**How an intern uses it:**
1. Open the playbook → find the task (Ctrl+F)
2. Copy the prompt inside the `--- COPY FROM HERE ---` block
3. Fill in the `[SQUARE BRACKET]` placeholders
4. Paste their document/data below
5. Send to Claude → get professional output

→ **[View Team Prompt Playbook](claude-desktop-projects/09-team-prompt-playbook.md)**

---

## 🗂️ All Claude Desktop Projects (System Prompts)

Each file below is a standalone Claude Desktop Project. Copy the instructions section into a new Project in Claude Desktop.

| File | Domain Covered |
|------|---------------|
| [00-SETUP-GUIDE.md](claude-desktop-projects/00-SETUP-GUIDE.md) | How to set up, connect Tally, privacy notes |
| [01-gst-compliance.md](claude-desktop-projects/01-gst-compliance.md) | GST — GSTR-1/3B/9/9C, ITC recon, notices, due dates, blocked credits |
| [02-income-tax-tds.md](claude-desktop-projects/02-income-tax-tds.md) | Income Tax + TDS — ITR forms, slabs, advance tax, 26AS, all TDS sections |
| [03-audit-assurance.md](claude-desktop-projects/03-audit-assurance.md) | Audit — all 21 CARO 2020 clauses, SA-315 risk, bank NPA norms, materiality |
| [04-mca-tp-fema.md](claude-desktop-projects/04-mca-tp-fema.md) | MCA + TP + FEMA — ROC filings, board resolutions, TP methods, FDI reporting |
| [05-advisory-payroll.md](claude-desktop-projects/05-advisory-payroll.md) | Advisory + Payroll — regime comparison, PF/ESIC, state PT, MSME 43B(h) |
| [06-client-firm-management.md](claude-desktop-projects/06-client-firm-management.md) | KYC, PMLA obligations, engagement letters (SA-210), fee management |
| [07-opensource-alternatives.md](claude-desktop-projects/07-opensource-alternatives.md) | Free/open-source options if you don't want Claude |
| [08-master-team-workspace.md](claude-desktop-projects/08-master-team-workspace.md) | Single all-in-one Project for the entire team |
| [09-team-prompt-playbook.md](claude-desktop-projects/09-team-prompt-playbook.md) | 30 standard prompts for daily CA office tasks |

---

## 🔌 Optional: Connect Tally for Live Data

The Tally MCP connector lets Claude read your Tally data directly — trial balance, ledger reports, stock reports. This is optional and only needed if you want live Tally data in Claude.

Setup takes about 15 minutes and requires Python (free). Full instructions in the [Setup Guide](claude-desktop-projects/00-SETUP-GUIDE.md#step-5-optional--connect-tally-for-live-data).

MCP connectors are also available for:
- GST Portal (read GSTR-1, GSTR-3B, GSTR-2B drafts)
- TRACES (download 26AS, TDS certificates)
- MCA21 (company profile, director details, filing status)

> These connectors are **read-only by default**. Any write/submit action requires explicit CA approval each time — a confirmation checklist is shown before anything is filed or posted.

---

## 🔒 Safety — Nothing Is Filed Without Your Approval

Claude will **never automatically file** any return, post to Tally, or send any communication without showing you a checklist and waiting for your approval. This is enforced at every step.

**Before any GST filing:**
```
GST FILING — YOUR APPROVAL REQUIRED

Return    : GSTR-3B
Client    : Example Pvt Ltd
GSTIN     : 37XXXXX1234Z5
Period    : April 2026
Tax Amount: Rs.2,34,500

Confirm before approving:
  [ ] GSTR-1 is filed for this period
  [ ] ITC reconciled with GSTR-2B
  [ ] Cash ledger balance is sufficient
  [ ] Client has authorised this filing

Approve = proceed  |  Deny = stop
```

**Before any Tally write:**
```
TALLY WRITE — YOUR APPROVAL REQUIRED
⚠  This action modifies accounting data.

Action       : Create 47 Purchase Vouchers
Company      : Example Infra Pvt Ltd
Total Debit  : Rs.18,42,000
Date Range   : 01 Apr 2026 to 30 Apr 2026

  [ ] Voucher amounts are correct
  [ ] Ledger heads are correctly mapped
  [ ] No duplicate entries

Approve = post to Tally  |  Deny = stop
```

---

## 📁 Repository Structure

```
claude-for-ca/
│
├── claude-desktop-projects/     ← START HERE for non-technical users
│   ├── 00-SETUP-GUIDE.md        ← How to set up Claude Desktop
│   ├── 01-gst-compliance.md     ← GST Project system prompt
│   ├── 02-income-tax-tds.md     ← Income Tax + TDS Project
│   ├── 03-audit-assurance.md    ← Audit & Assurance Project
│   ├── 04-mca-tp-fema.md        ← MCA, Transfer Pricing, FEMA
│   ├── 05-advisory-payroll.md   ← Advisory, Payroll, MSME
│   ├── 06-client-firm-management.md  ← KYC, Engagement, Fees
│   ├── 07-opensource-alternatives.md ← Free alternatives to Claude
│   ├── 08-master-team-workspace.md   ← All-in-one team Project
│   └── 09-team-prompt-playbook.md    ← 30 standard prompts for daily work
│
├── mcp-connectors/              ← Optional live data connectors (Python)
│   ├── tally/                   ← Tally Prime / ERP 9 connector
│   ├── gst-portal/              ← GST Portal Selenium connector
│   ├── traces/                  ← TRACES TDS portal connector
│   └── mca21/                   ← MCA21 V3 API connector
│
├── gst-compliance/              ← Claude Code plugin (for technical users)
├── income-tax/                  ← Claude Code plugin
├── tds-compliance/              ← Claude Code plugin
├── audit/                       ← Claude Code plugin
├── mca-secretarial/             ← Claude Code plugin
├── transfer-pricing/            ← Claude Code plugin
├── fema-compliance/             ← Claude Code plugin
├── payroll-compliance/          ← Claude Code plugin
├── advisory-ca/                 ← Claude Code plugin
├── client-onboarding/           ← Claude Code plugin
├── ca-student/                  ← Claude Code plugin
├── firm-management/             ← Claude Code plugin
├── document-intake/             ← Claude Code plugin
├── shared/                      ← Core HITL hooks, memory bank, audit log
│
├── references/
│   └── ca-compliance-calendar.md  ← Full Indian CA compliance calendar
│
└── CLAUDE.md                    ← Firm profile template (fill this in)
```

---

## 👨‍💻 For Technical Users — Claude Code Plugin Suite

If you use Claude Code (VS Code extension or terminal), you get the complete automation experience: skill invocations, compliance calendar monitoring, firm memory, and a full audit trail.

**16 plugins | 59 skills | 8 monitoring agents | 4 MCP connectors**

```bash
git clone https://github.com/eurth/claude-for-ca
cd claude-for-ca

# One-time firm onboarding
claude install plugin ./shared
claude install plugin ./cold-start
claude "/cold-start:onboard-firm"

# Install the plugins you need
claude install plugin ./gst-compliance
claude install plugin ./income-tax
claude install plugin ./tds-compliance
claude install plugin ./audit
```

Then use skills like:
```
/gst-compliance:gstr3b-review
/income-tax:notice-analyser
/tds-compliance:26as-reconciliation
/audit:caro-2020-checklist
```

See each plugin folder's `README.md` for the full skill list.

---

## ❓ Frequently Asked Questions

**Do I need to pay for Claude?**
The free Claude plan has limits (message caps). For daily professional use, Claude Pro (~Rs.1,700/month) is recommended for one person. For a team, Claude Teams (~Rs.2,500/user/month) lets multiple staff share Projects.

**Do I need to install anything?**
For Claude Desktop: just download and install the app — it works like any normal software. No Python, no Git, no terminal.
For Tally connector: needs Python (free, 10-minute install). Instructions in the [Setup Guide](claude-desktop-projects/00-SETUP-GUIDE.md).

**Can Claude file GST returns or TDS returns automatically?**
No. Every filing action requires explicit CA approval. This is enforced in the system and cannot be bypassed.

**Is client data safe?**
Claude processes data on Anthropic's servers (SOC 2 compliant). For sensitive work, avoid pasting actual PAN/Aadhaar numbers — use client descriptions instead. Claude Pro/Teams users' conversations are not used for model training per Anthropic's policy.

**What if my PDF is in Telugu or Hindi?**
Claude reads multilingual PDFs. Output is in English (or whichever language you ask for).

**Is this affiliated with Anthropic or ICAI?**
No. This is an independent open-source project. It uses Anthropic's Claude API but is not endorsed by Anthropic or the Institute of Chartered Accountants of India.

**My client received a notice I've never seen before. Can Claude still help?**
Yes — paste the notice text and describe the situation. Claude will explain the notice, identify the section and its implications, and help draft a response.

---

## 🤝 Contributing

This repository is open to the CA community. Contributions welcome:

- **New prompts for the playbook** — If you have a task that's not covered, add a prompt and submit a pull request
- **Better Excel column formats** — If your firm uses specific column layouts, share them
- **State-specific compliance** — Professional tax rates, state VAT specifics, local body taxes
- **Bug reports / corrections** — Tax rates change, sections get amended — flag anything outdated
- **Translations** — Prompts in Telugu, Hindi, Tamil for regional teams

**How to contribute:**
1. Fork this repository on GitHub
2. Make your changes
3. Submit a Pull Request with a brief description

**For suggestions without coding:** Open a GitHub Issue — describe what you need and we'll add it.

---

## Credits

Conceptualised and built by **[EurthTech](https://eurth.in)**
Designed by **CogentDeFi**
Mentored by **CA Butchi Babu, Gorantla Associates, Andhra Pradesh**

---

## License

[Apache 2.0](LICENSE) — free to use, modify, and deploy in your practice. Attribution appreciated.

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
