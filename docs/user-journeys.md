# User journeys — inputs and outputs

Every journey: **select entity** → (GSTIN / period if needed) → **attach documents** → **Run** → **review** → **download or send for Partner approval**.

Staff do not choose a model or a skill ID. The feature name is the job.

---

## A. Intern — invoice week

**Scope:** legal entity + GSTIN + month  

**Feature:** Extract invoices  

**In**
- Purchase invoice PDFs (including scanned and password-protected)
- Optional sales invoices / credit notes / debit notes

**Out**
- Purchase / sales register table (Excel)
- JSON `purchase_invoice` rows
- Exception report (GSTIN checksum, tax mismatch, duplicates, TDS flag)

**Next:** same artifacts feed Master accounts and Tally import for that GSTIN+month.

---

## B. Intern — bank

**Scope:** legal entity + month  

**Feature:** Process bank statement  

**In**
- Bank or credit-card PDF
- Bank name, account last-4, period, password if any
- Optional: purchase register from A (to match payments)

**Out**
- Transaction ledger with suggested Tally heads
- Unmatched / review items
- BRS working if opening/closing given

---

## C. Manager — books pack

**Scope:** legal entity + FY/month  

**Features:** Master accounts workbook → Tally import file  

**In**
- Registers and bank ledger from A and B (auto-attached if keys match)

**Out**
- `Master Accounts FY… — [Company].xlsx` (11 sheets: SUMMARY, PURCHASE, SALES, BANK, CASH, GST, TDS, PAYABLES, RECEIVABLES, P&L, BS)
- `tally_import_[period]_[date].xml`
- HITL: Partner must approve Tally XML before intern treats it as final
- Human imports XML in Tally: Gateway → Import Data → Vouchers

---

## D. Manager — monthly GST

**Scope:** GSTIN + return period  

**Features:** Reconcile ITC → Review GSTR-1 → Review GSTR-3B  

**In**
- GSTR-2B Excel/JSON (upload)
- Purchase register (from A if same GSTIN+month)
- GSTR-1 / sales totals
- Cash ledger balance (typed or screenshot)

**Out**
- ITC recon (OK / 2B-only / PR-only / amount-diff / time-barred / blocked)
- Vendor follow-up email drafts
- GSTR-3B working + pre-filing checklist
- Status `pending_approval` for Partner

**Context reuse:** purchase register from journey A is injected automatically.

---

## E. Manager — TDS / ITR

**Scope:** legal entity (PAN) + FY / quarter  

**Features:** Reconcile 26AS, TDS default check, TDS quarterly return, Form 16 data, Review ITR, Advance tax  

**In**
- 26AS / AIS PDF or Excel
- Books TDS / income ledger
- Challans (BSR, date, serial)
- Salary register (Form 16)
- Estimated income (advance tax)

**Out**
- 26AS match tables
- 201(1A) / 234E workings
- Form 16 Part B data sheet
- ITR pre-filing checklist vs 26AS
- Advance-tax instalment schedule

---

## F. Partner — notice

**Scope:** legal entity (and GSTIN if GST notice)  

**Features:** GST notice **or** Income-tax notice  

**In**
- Notice PDF (DRC-01, SCN, 142/143/148/156, etc.)
- DIN, date received, known facts

**Out**
- Plain-language summary and deadline
- Draft reply on firm letterhead tone
- Notice row on the entity file
- Approval required before “ready to send”

---

## G. Audit / MCA / TP / payroll / advisory

Same workpack loop. Typical **in**: trial balance, financials, CARO evidence, MCA master data, payroll ECR, Udyam facts. Typical **out**: CARO drafts, workpapers, resolutions, 3CEB pack, PF/ESIC recon, regime comparison. All **drafts**.

---

## H. Onboarding a client

**Features:** Add client (group + entity + GSTINs), KYC checklist, Engagement letter  

**In**
- PAN, one or more GSTINs, CIN, TAN, contacts, KYC scans, engagement type and fee

**Out**
- Entity file with registrations
- KYC document status
- SA-210 draft for Partner

---

## I. Intern playbook forms (A1–H3)

Placeholders become form fields. Paste/upload still allowed.

| ID | In | Out |
|----|----|-----|
| A1–A3 | Invoice text/PDF | Purchase or sales Excel row(s) |
| A4 | Bank statement | Txn table + likely ledger |
| A5 | Contract | Terms extract + CA flags |
| A6 | Salary slips | Payroll register |
| B1–B4 | Lists / figures | Expense, TDS working, GSTR-3B working, IT computation |
| C1–C6 | Names, dates, amounts | Emails / notice reply (draft) |
| D1–D4 | Ledger / TB | Anomalies, AP ageing, BRS, MIS |
| E1–E3 | Month / invoices / 26AS | Calendar, invoice GST check, 26AS recon |
| F1–F3 | Notes | Status, actions, file note |
| G1–G4 | Dates, amounts, state | Late fee, 201(1A), PF/ESIC, PT |
| H1–H3 | Facts | ITR form, TDS rate, HSN/SAC |

---

## Six pilots implemented in this repo

| # | Staff name | Feature id | Primary in | Primary out |
|---|------------|------------|------------|-------------|
| 1 | Extract invoices | `pdf-data-extractor` | Invoice PDFs | Register + exceptions |
| 2 | Process bank statement | `bank-statement-processor` | Bank PDF | Ledger + exceptions |
| 3 | Tally import file | `tally-import-builder` | Register JSON | XML + HITL |
| 4 | Review GSTR-3B | `gstr3b-review` | Period figures / registers | Working + HITL |
| 5 | Notice (GST or IT) | `notice-triage` | Notice PDF | Summary + draft + HITL |
| 6 | What do I need? | `discover` | Description of the task | Suggested feature |

`notice-analysis` procedure is merged into the Notice workpack (portal detected from the PDF / a form field).
