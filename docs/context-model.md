# Context model — group, entity, GSTIN, workpack

Staff never “manage prompt context”. The UI always has a selected **legal entity**. GST features also require a **registration (GSTIN)** and a **period**. The runtime injects the rest.

## Why the old model fails

`clients` in `shared/mcp-server/memory_bank_server.py` is one row with a single `gstin` TEXT column. A group with three companies and multiple GSTINs cannot be represented. Master Excel and Tally XML are one-company artifacts. That is correct for a *file*, but the **master data** must be hierarchical.

## Hierarchy

```
FirmTenant (Gorantla Associates)
  └── ClientGroup (optional, e.g. “Infra group”)
        └── LegalEntity (PAN, CIN, constitution, Tally company name)
              ├── Registration GSTIN (state, monthly/QRMP, ISD/SEZ/branch)
              ├── Registration TAN
              └── Registration PF / ESIC establishment
                    └── Period (FY / month / quarter)
                          └── Workpack (one feature run)
                                ├── Artifacts (inputs + outputs)
                                ├── Thread (optional chat)
                                └── Approval (if filing-class)
```

| Node | Identity | Features that bind here |
|------|----------|-------------------------|
| FirmTenant | ICAI firm, GSTIN of the practice | Settings, users, letterhead, LLM keys |
| ClientGroup | Display name only | Roll-up dashboard (read-only) |
| LegalEntity | PAN (unique per tenant), CIN | ITR, 26AS, tax audit, CARO, engagement, fees |
| Registration | GSTIN or TAN or PF code | GSTR-1/3B/2B, TDS returns, payroll |
| Period | `2026-04` or `FY2025-26` or `Q1` | Almost every compliance workpack |
| Workpack | Feature slug + entity + registration + period | Isolation of chat and files |
| Artifact | Typed blob (`purchase_register`, `gstr2b_excel`, …) | Reused by later features |
| Thread | Messages for this workpack only | Switching entity starts a new thread |

## Isolation rules

1. GST work cannot read another GSTIN’s GSTR-2B or purchase register.
2. ITR / 26AS run at **entity (PAN)** scope; they may *list* GSTINs but not mix 2B files.
3. Group dashboards aggregate counts and dues only.
4. Tenant isolation is absolute (every query filtered by `firm_id`).

## How context is injected

On every **Run**:

1. Load firm profile + user role.
2. Load legal entity + selected registration + period.
3. Load open notices and calendar tasks for that scope.
4. Load **prior artifacts** with the same `(entity_id, registration_id, period, artifact_type)`.
   - Example: Extract invoices for GSTIN X / Apr 2026 writes `purchase_register`. Reconcile ITC and Review GSTR-3B for the same keys attach that register automatically (staff can override).
5. Build the system bundle: skill markdown + JSON context (no `${CLAUDE_PLUGIN_ROOT}`).
6. Persist model output as new artifacts on the same keys — not only as chat.

## Workpack status

`draft` → `running` → `needs_review` → `pending_approval` → `approved` → `exported`

There is no `filed` except a **manual** Partner checkbox: “I have filed this outside the app” (updates the compliance calendar only).

Filing-class features (GSTR-3B pack, notice reply, Tally XML, ITR pack, TDS return pack, MCA form pack) **always** enter `pending_approval` with the HITL checklist from `shared/bin/hitl-*.sh`.

## Artifact types (do not invent parallels)

From existing intake skills:

| type | Produced by | Consumed by |
|------|-------------|-------------|
| `purchase_invoice` / `purchase_register` | Extract invoices | Master accounts, Tally XML, ITC recon, GSTR-3B |
| `sales_register` | Extract invoices (sales) | GSTR-1, Master accounts, GSTR-3B |
| `exception_report` | Extract invoices, bank | Manager review |
| `bank_ledger` | Process bank statement | Master accounts, BRS, Tally XML |
| `master_accounts_xlsx` | Master accounts workbook | Month-end, GSTR-9 |
| `tally_xml` | Tally import file | Human import in Tally |
| `gstr2b_excel` | Staff upload | ITC recon |
| `notice_pdf` | Staff upload | GST notice / IT notice |
| `draft_reply` | Notice features | Partner approval |
| `gstr3b_working` | Review GSTR-3B | Partner approval |

## Intern vs Partner context

Interns see only the selected entity’s documents and playbook forms. Partners see the approval inbox across entities. Model routing (`effort: low|high`) is Partner configuration; interns do not pick models.
