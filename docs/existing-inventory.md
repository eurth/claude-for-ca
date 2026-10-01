# Existing toolkit inventory — Claude for CA

Source of truth for what this repository already contains before the for-ca web app. Skill procedure bodies are reused; Claude Desktop / Claude Code install paths are not.

**Counts (as of implementation):** 16 marketplace plugins (15 with `plugin.json` + `ca-builder-hub` skill-only) · **60** `SKILL.md` files · **8** agents · **6** managed-agent cookbooks · **4** MCP connector packages · **10** Claude Desktop project files · **33** playbook copy-blocks (footer still says 30).

Two delivery surfaces over the same knowledge:

- **Claude Desktop** — paste instructions from `claude-desktop-projects/` plus the team playbook. No install beyond the Claude app.
- **Claude Code plugins** — `claude install plugin`, slash commands, SQLite memory bank, HITL hooks.

---

## Claude-only glue (do not port as-is)

| Mechanism | Where | Why the web app cannot use it |
|-----------|--------|-------------------------------|
| `model: claude-*` | Every SKILL.md / agent.yaml; `scripts/validate.py` | Validator and runtime assume Anthropic model IDs |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` | Skills, HITL scripts, `.mcp.json` | Paths only exist inside Claude Code |
| `` !`python3 ...` `` interpolators | Skill bodies (firm context inject) | Other runtimes print this as literal text |
| `mcp__memory_bank__*` allowed-tools | Skill frontmatter | Claude Code tool IDs |
| `hooks.json` PreToolUse / SessionStart | `shared/hooks/hooks.json` | Claude Code hook schema |
| `claude install plugin` + marketplace | `.claude-plugin/` | Web app loads `packs/` + a feature catalog |
| Claude Desktop Projects | `claude-desktop-projects/01–08` | Become domain personas / section home pages |

---

## Memory bank (keep the ideas, not SQLite)

File: `shared/mcp-server/memory_bank_server.py`

| Table | Purpose |
|-------|---------|
| `firm_profile` | Single-row firm identity, GSTIN, Tally DSN, software stack |
| `clients` | Flat client: one PAN, **one GSTIN**, one Tally company |
| `notices` | Statutory notices, demand, draft path, status |
| `compliance_calendar` | Form type, period, due date, filed status |
| `audit_trail` | Append-only tool/session log |

**Tools:** `get/save_firm_profile`, `get/list/save_client`, `log/update/list_notices`, `log_compliance_event`, `mark_filing_complete`, `get_due_dates`, `query_audit_trail`, `log_audit_entry`.

**Schema gap:** no group, no parent entity, no extra GSTIN/branch/SEZ/ISD, no related-party table. Subsidiaries appear only inside audit/FEMA *content*.

---

## HITL scripts

`shared/hooks/hooks.json` + `shared/bin/`

| Script | Trigger (Claude Code) | Web-app equivalent |
|--------|----------------------|-------------------|
| `hitl-gst-filing.sh` | GST portal submit/file | Approval type `gst_filing` |
| `hitl-tds-filing.sh` | TRACES file/submit | Approval type `tds_filing` |
| `hitl-itr-filing.sh` | e-filing submit | Approval type `itr_filing` |
| `hitl-mca-filing.sh` | MCA file/submit/sign | Approval type `mca_filing` |
| `hitl-tally-write.sh` | Tally create/write/post | Approval type `tally_write` (threshold ₹1 lakh) |
| `audit-log.sh` | PostToolUse all MCP | `audit_trail` row |
| `load-firm-context.sh` | SessionStart | Injected firm+entity bundle on every workpack |

v1 of the web app **never files**. These become Partner checklists before a pack is marked “ready to file outside the app” or “ready to import into Tally”.

---

## MCP connectors (v2 office agent only)

| Package | Tools (implemented) | HITL writes |
|---------|---------------------|-------------|
| `mcp-connectors/gst-portal/gst_portal_mcp.py` | `get_gstr1_draft`, `get_gstr3b_summary`, `get_gstr2b`, `submit_gstr1`, `submit_gstr3b` | submits |
| `mcp-connectors/traces/traces_mcp.py` | `get_26as`, `get_tds_certificates`, `get_csi_file`, `file_tds_return` | file return |
| `mcp-connectors/tally/tally_mcp_wrapper.py` | `get_trial_balance`, `get_ledger_report`, `get_balance_sheet`, `get_stock_report`, `create_voucher` | `create_voucher` |
| `mcp-connectors/mca21/mca21_mcp.py` | `get_company_profile`, `get_director_details`, `get_filing_status`, `file_mca_form` | file e-form |

**Porting bugs (do not copy):** Tally README lists `get_ledgers`, `search_party`, `get_vouchers` that the wrapper does not fully implement. KYC skill calls `mcp__memory_bank__add_client`; server exposes `save_client`. Folder `gst-compliance/skills/itc-recon` YAML name is `itc-reconcile`.

Gmail MCP (`search_emails`, `get_email`, `download_attachment`) is used by email-invoice-fetch — **v2** (OAuth).

---

## Document pipeline (today)

```
email-invoice-fetch → PDFs on disk
pdf-data-extractor  → markdown table / JSON + exception list
bank-statement-processor → categorised table / BRS / optional XML
        ↓
master-accounts-sheet → Master Accounts FY….xlsx (11 sheets)
tally-import-builder  → tally_import_[period]_[date].xml (+ HITL)
```

All of this assumes **one company / one GSTIN / one Tally company**.

---

## Skill catalog (all 60)

Dispatcher skills named `review` become **section home pages** in the web app, not LLM jobs.

### shared — claude-for-ca-core

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `firm-context` | Session briefing | Firm already onboarded | Firm summary, 30-day dues, open notices | Reminder only |

### cold-start

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `onboard-firm` | Set up this firm | Firm identity, software stack, seed clients, HITL threshold | Firm profile + calendar seed | Explains filing pause |
| `add-client` | Add client | Legal name, PAN, GSTIN, TAN, CIN, type, industry, contacts, Tally company, filings | Client row + calendar tasks | None |

### document-intake

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `pdf-data-extractor` | Extract invoices | Invoice/CN/DN PDFs (scanned, password OK); bank PDFs also accepted | Excel-ready table, `purchase_invoice` JSON, exception list | None |
| `bank-statement-processor` | Process bank statement | Bank PDF, bank name, A/c last-4, period, password | Txn table, categories, suggested ledgers, BRS, exceptions | None |
| `email-invoice-fetch` | Fetch invoices from email | Period, inbox, Gmail MCP | PDF folder + hit list | v2 |
| `master-accounts-sheet` | Master accounts workbook | Extracted invoices + bank table, company, FY, opening balances | 11-sheet xlsx (SUMMARY, PURCHASE, SALES, BANK, CASH, GST, TDS, PAYABLES, RECEIVABLES, P&L, BS) | None |
| `tally-import-builder` | Tally import file | Extractor JSON / Excel paste; ledger names | `tally_import_[period]_[date].xml` | Yes — never live-post without approval |

### gst-compliance

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | GST home | Memory bank | Due dates, nav | — |
| `gstr1-review` | Review GSTR-1 | GSTIN, period, sales register or portal draft | Review summary, exceptions | Do not file |
| `gstr3b-review` | Review GSTR-3B | GSTIN, period, QRMP flag, outward/ITC, cash ledger | Tax working, interest, pre-filing checklist | Do not submit |
| `itc-reconcile` | Reconcile ITC (GSTR-2B) | GSTR-2B Excel/JSON; purchase register | Recon codes (OK / 2B-only / PR-only / AMT-DIFF / TIME-BAR / BLOCKED), vendor emails | CA sign-off before claim |
| `notice-triage` | GST notice | Notice PDF, DIN, dates, demand | Summary, root cause, letterhead draft, notice row | Draft only |
| `annual-return` | GSTR-9 / 9C | FY, month-wise 1 & 3B, books, ITC ledger | Difference tables, 9C recon, certification draft | Partner; 9C is CA certification |
| `gst-audit` | GST audit (65/66) | Audit notice + books/returns | Scrutiny checklist, representation draft, DRC-03 calc | Partner |

**Agents:** `gst-duedate-watcher` (daily), `annual-return-reminder` (Oct–Mar).

### income-tax

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Income tax home | Memory bank | Dashboard | — |
| `itr-review` | Review ITR | PAN, AY, form, 26AS/AIS, deductions | Mismatch report, tax computation, pre-filing checklist | CA + e-verify |
| `notice-analysis` | Income-tax notice | Notice PDF, DIN, dates | Plain-language summary, reply draft, deadlines | CA before send |
| `advance-tax` | Advance tax | Estimated income, TDS, prior instalments | Schedule, 234B/234C, payment advice | Confirm estimates |
| `capital-gains` | Capital gains | Per-asset dates/costs | CG schedule, set-off | CA before filing |
| `tax-audit-3cd` | Tax audit 3CD | Books/ledgers, clause facts | 44-clause disclosures, disallowance schedules | Never certify unread |
| `search-survey` | Search / survey | Situation, premises, seized docs | Rights guidance, preservation checklist | Specialist/advocate |

**Agents:** `itr-season-tracker` (Jul–Oct), `advance-tax-watcher` (15 Jun/Sep/Dec/Mar).

### tds-compliance

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | TDS home | Memory bank | Dashboard | — |
| `default-check` | TDS default check | Payment ledger, challans, TAN, quarter | Defaults, 201(1A) interest | None (analysis) |
| `26as-recon` | Reconcile 26AS | 26AS/AIS file; books | Match / not-in-books / not-in-26AS | ITR credit only per 26AS |
| `form-16-generator` | Form 16 / 16A data | Salary register, TRACES Part A, deductions | Part B draft | Verify before issue |
| `quarterly-return` | TDS quarterly return | TAN, challans (BSR/date/serial), deductees | 234E, pre-filing checklist | Filing HITL |

**Agents:** `tds-deadline-watcher` (deposit 7th + quarterly + Form 16).

### audit

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Audit home | Memory bank | Engagements | — |
| `caro-review` | CARO 2020 | Working papers per clause | 21 clause drafts + summary | Evidence-backed |
| `risk-matrix` | Audit risk matrix | Industry, financials, controls | Materiality, SA-315 matrix | — |
| `workpaper-draft` | Workpapers | TB / area data | Lead schedules, representation letter, completion checklist | — |
| `bank-audit-lfar` | Bank audit / LFAR | Advances, IRAC, stock statements | NPA review, LFAR responses | Regulatory |
| `internal-audit` | Internal audit | Cycle scope, prior findings | Plan, IAR | Objective findings |

**Agents:** `audit-completion-tracker`.

### mca-secretarial

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | MCA home | Memory bank | ROC calendar | — |
| `filing-tracker` | ROC filing tracker | CIN, AGM date, FY, filed status | Status board, late fees | File ops HITL (v2) |
| `resolution` | Board resolution | Company, type, names/DINs/amounts | Resolution text, MGT-14 checklist | — |
| `annual-compliance` | Annual company compliance | FS, board facts, Sec 134 | AGM notice, directors’ report checklist | — |
| `charge-registry` | Charge registry | CIN, holder, date, amount, asset | CHG-1/4 pack, late-fee guidance | — |

**Agents:** `roc-calendar-watcher`.

### transfer-pricing

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | TP home | Memory bank | Nav | — |
| `form-3ceb` | Form 3CEB | International/SDT list, methods, comparables | Para-wise drafts | CA signature |
| `tp-documentation` | TP documentation | Group structure, FAR, financials | Rule 10D study | 271AA risk |

### fema-compliance

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | FEMA home | Memory bank | Nav | — |
| `fdi-compliance` | FDI (FC-GPR / FC-TRS) | Investee, investor, allotment/transfer, pricing | Checklists, pricing-norm notes | Compounding risk |
| `odi-compliance` | ODI / APR | Indian investor, overseas JV/WOS | ODI/APR checklists | AD bank |

### payroll-compliance

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Payroll home | Memory bank | Calendar | — |
| `pf-recon` | PF / ECR | Salary register Basic+DA, joiners/exits, month | PF register, ECR checklist | Trust money |
| `esic-recon` | ESIC | Wages ≤ ceiling, month | ESIC register | — |
| `professional-tax` | Professional tax | State, employee list, gross | PT table + deposit authority | — |

**Agents:** `payroll-calendar-watcher`.

### advisory-ca

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Advisory home | Memory bank | Nav | — |
| `tax-planning` | Tax planning | Income profile, investments | Old vs new regime, year-end checklist | GAAR caution |
| `msme-advisory` | MSME / Udyam | Turnover, MSME vendors, payment dates | Udyam guidance, 43B(h) analysis | — |

### client-onboarding

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Onboarding home | — | KYC → EL → add-client flow | — |
| `kyc-checklist` | KYC checklist | Entity type | Doc checklist, PMLA log | PMLA duties |
| `engagement-letter` | Engagement letter | Client, type, fee, FY | SA-210 draft | Sign before statutory work |

### firm-management

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Practice home | Fees / KPIs | Monthly review checklist | — |
| `fee-tracker` | Fee tracker | Billing/collection | Register, WIP, reminder drafts | — |

### ca-student (optional module)

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `review` | Student hub | — | Nav | — |
| `articleship-log` | Articleship diary | Daily work, hours by area | Diary vs ICAI minima | — |
| `exam-prep` | Exam prep | Level, paper, month | Notes, study plan | — |

### ca-builder-hub

| Skill | Staff feature name | Inputs | Outputs | HITL |
|-------|-------------------|--------|---------|------|
| `discover` | What do I need? | Natural-language task | Route to the right feature | — |

---

## Watchers / cookbooks

| Agent / cookbook | Cadence | Web-app job |
|------------------|---------|-------------|
| gst-duedate-watcher | Daily, 7-day window | Scheduled due-date digest |
| annual-return-reminder | Oct–Mar | Seasonal |
| tds-deadline-watcher | Daily / 15-day | Deposit + 24Q/26Q |
| advance-tax-watcher | Instalment windows | 15 Jun/Sep/Dec/Mar |
| itr-season-tracker | Jul–Oct | Filed vs pending |
| roc-calendar-watcher | Ongoing | ROC 7/30 days |
| payroll-calendar-watcher | Daily | PF 15th, ESIC, PT |
| audit-completion-tracker | Audit season | Milestone board |

Cookbooks additionally **disallow** submit/file tools. The web app must keep the same deny-by-default.

---

## Claude Desktop projects

| File | Role in web app |
|------|-----------------|
| `00-SETUP-GUIDE.md` | Historical; replaced by product login + firm setup |
| `01-gst-compliance.md` | GST section persona |
| `02-income-tax-tds.md` | IT + TDS persona |
| `03-audit-assurance.md` | Audit persona |
| `04-mca-tp-fema.md` | MCA/TP/FEMA persona |
| `05-advisory-payroll.md` | Advisory + payroll persona |
| `06-client-firm-management.md` | KYC / fees persona |
| `07-opensource-alternatives.md` | Historical; LLM gateway replaces this |
| `08-master-team-workspace.md` | Default firm workspace tone |
| `09-team-prompt-playbook.md` | **33 forms** (A1–H3), not free chat |

Playbook IDs: A1–A6 documents; B1–B4 Excel workings; C1–C6 emails; D1–D4 accounts; E1–E3 compliance; F1–F3 office; G1–G4 calculations; H1–H3 lookups.

---

## What the web app must preserve

1. Every filing-class action is a draft + Partner checklist.
2. Audit trail of who ran what, on which entity, which model, which files.
3. Skill procedure text (law, checklists, output shapes) stays in markdown packs.
4. Artifact types already named by intake skills (`purchase_invoice` JSON, exception list, Master Accounts xlsx, Tally XML) are the interchange format between features.
