# Staff flows — expected results

Seed login: `partner@gorantla.local` / `changeme`. Client: Example Traders Pvt Ltd. Prefer GSTIN `37AACTE1234F1Z5` (Head office). Period `2026-04`.

## TC-01 Login

Open `/login`, sign in as Partner. Home shows firm **Gorantla Associates**.

## TC-02 Extract invoices

1. Work → Extract invoices (do **not** wait for an auto-run).
2. Upload `samples/invoices/INV-ST-1042-Sharma-Traders.pdf` (you can multi-select RK/88 and the duplicate).
3. Run job.
4. Expect a **purchase register table** with Sharma Traders, ST/1042, taxable 10000, CGST/SGST 900, total 11800. Ravi Kirana RK/88 shows IGST 900. Duplicate ST/1042 is listed under Exceptions.
5. Run again after more uploads: empty `{ "rows": [] }` blocks must **not** pile up — only the latest working.

## TC-03 Bank statement

1. Work → Process bank statement.
2. Upload `samples/bank/HDFC-50200011223344-Apr-2026.pdf`, then Run.
3. Expect a ledger **table** with 12 April 2026 rows and unmatched UPI/cash notes. Empty ledgers from earlier runs should not remain.

## TC-04 GSTR-3B (reuses purchase register)

After TC-02 for the same GSTIN + `2026-04`, start **Review GSTR-3B**. Status should become pending approval. Approvals inbox shows the GSTR-3B checklist. Partner can Approve / Deny. Nothing is filed.

## TC-05 Notice router

Start **What do I need?** with note “Client sent a GST DRC-01”. Expect a suggestion toward notice triage.

## TC-06 Gemma / fallback

If the summary looks empty or the job says “Could not complete”, the current free endpoint failed. Re-run. Gateway tries Nemotron Super 120B first, then Gemma 4 26B, Gemma 4 31B, then `openrouter/free`. Partner-only `model_used` on the workpack shows which one answered. Google-hosted Gemma is often 429/502/504 — do not pin it as the default.
