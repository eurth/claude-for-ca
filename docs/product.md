# Product — for-ca (CA Practice)

Staff-facing product for Indian CA firms. First tenant: **Gorantla Associates**. Later tenants: other CA firms on the same Eurth-hosted app. Chrome shows the **firm name**, never “Claude”, model IDs, or skill slugs.

Working name in code: `for-ca`. Public URL (planned): `https://ca.eurthtech.com`.

---

## Who it is for

| Role | What they do | What they cannot do |
|------|----------------|---------------------|
| **Partner** | Approve high-liability packs, notices, Tally XML, firm settings, LLM keys, HITL threshold | The app never files for them |
| **Manager** | Run all compliance/audit/advisory features, assign work, mark in review | Cannot skip Partner approval on filing-class packs |
| **Article / intern** | Extract invoices and bank statements, fill playbook forms, upload KYC | Cannot mark a pack “ready for CA review” on filing-class features |

---

## Product principles

1. Work is always scoped to a **client group → legal entity → GSTIN/TAN** and a **period**.
2. Features are named jobs (“Review GSTR-3B”), not prompts.
3. Chat is optional and still bound to the same entity and workpack.
4. Outputs are files and tables on the entity file, not a transcript the intern must copy.
5. Nothing is filed to GST/IT/TDS/MCA. Nothing is posted live to Tally in v1.
6. Buttons say **Download for Tally** and **Mark ready for CA review**.

---

## v1 screens

| Screen | Job |
|--------|-----|
| Sign in | Firm staff login |
| Home | This week’s dues, assigned workpacks, approvals waiting |
| Clients | Groups, entities, GSTINs |
| Entity file | KYC, notices, documents, workpacks, artifacts |
| Features | Gallery of named jobs (from the skill catalog) |
| Workpack | Upload → run → review → download / send for approval |
| Approvals | Partner HITL checklists |
| Audit log | Who ran what, which model, which client |
| Firm settings | Users, roles, letterhead, HITL amount, LLM keys (Partner only) |

---

## Feature names staff see (v1 pilots + later)

### Daily documents
- Extract invoices
- Process bank statement
- Master accounts workbook
- Tally import file
- Fetch invoices from email *(v2)*

### GST
- Review GSTR-1
- Review GSTR-3B
- Reconcile ITC (GSTR-2B)
- GST notice
- GSTR-9 / 9C
- GST audit (65/66)

### Income tax & TDS
- Review ITR
- Income-tax notice
- Advance tax
- Capital gains
- Tax audit 3CD
- Search / survey
- TDS default check
- Reconcile 26AS
- Form 16 / 16A data
- TDS quarterly return

### Audit, MCA, TP, FEMA, payroll, advisory
- CARO 2020, audit risk matrix, workpapers, bank audit / LFAR, internal audit
- ROC filing tracker, board resolution, annual company compliance, charge registry
- Form 3CEB, TP documentation
- FDI (FC-GPR / FC-TRS), ODI / APR
- PF / ECR, ESIC, professional tax
- Tax planning, MSME / Udyam
- KYC checklist, engagement letter, fee tracker
- What do I need? (router)

Playbook items A1–H3 appear as **simple forms** on the intern home (extract one invoice, GSTR-3B working, document-request email, etc.).

---

## v1 vs v2

| | v1 (this build) | v2 |
|--|-----------------|-----|
| Data in | File upload | Office agent: Tally ODBC, GST portal, TRACES, MCA, Gmail |
| Data out | Excel, Tally XML download, draft Word/PDF | Same + optional live post after HITL |
| Filing | Never | Still HITL; agent only after Partner approve |
| Models | Anthropic / OpenAI / Gemini via gateway | Same + optional local |
| Tenancy | Schema ready; Gorantla seeded | More firms onboard |

---

## Non-goals (v1)

- Streamlit or Claude Desktop as the product UI
- Auto-filing or unsupervised Tally posting
- Fine-tuned local tax model as default
- Wrapping all 60 skills before the six pilots work in daily use
- Showing token counts or model names to interns
