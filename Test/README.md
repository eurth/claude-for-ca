# for-ca test pack

Local verification for the staff app: OpenRouter key, free-model fallbacks, sample GST invoices / bank statements, API scripts, and Playwright.

## What was verified (1 Oct 2026)

| Check | Result |
|--------|--------|
| API unit tests (`pytest apps/api/tests`) | Mock provider; no key required |
| OpenRouter key | **Valid** |
| `nvidia/nemotron-3-super-120b-a12b:free` | **Reliable — 200 + "OK"** (default) |
| `google/gemma-4-26b-a4b-it:free` | **Works when Google is up** (200 this run; previously **502**). Fallback #2 |
| `google/gemma-4-31b-it:free` | **Unreliable** — 504 aborted / Google AI Studio **429**. Do not pin |
| `openrouter/free` | Router; **OK this run** (landed on 31B) but **504** when Google is down. Last fallback |
| Other catalog `:free` IDs (Qwen, Liquid, Ling, Poolside, Dots, extra Nemotron, Inkling, Cohere) | **Unavailable** (404 guardrail / 403 harness-only) |
| Playwright (`Test/playwright`) | **3 passed** — login, invoice extract, bank upload |

Gemma free is flaky on Google AI Studio. Default model is **Nemotron Super 120B free**. If that fails, gateway tries Gemma 4 26B, Gemma 4 31B, then `openrouter/free`. Empty replies, 404, 429, 502–504 skip to the next model.

Bank jobs keep a **deterministic ledger parser** if the model returns scratchpad instead of JSON.

Full notes: `results/FINDINGS.md`.

## How to run

API + web must already be up (`http://127.0.0.1:8000` and `http://127.0.0.1:3000`). Key stays in repo-root `.env` (gitignored).

```bash
# 1) Unit tests (mock)
python -m pytest apps/api/tests -q

# 2) Sample PDFs
python Test/scripts/generate_samples.py

# 3) Ping free models (writes Test/results/openrouter_probe.json)
python Test/scripts/verify_openrouter.py

# 4) Live extract: upload invoice + bank PDF and run jobs
python Test/scripts/run_live_extract.py

# 5) Playwright (from Test/playwright)
cd Test/playwright
npm install
npx playwright install chromium
npx playwright test
```

## Samples

| File | Use |
|------|-----|
| `samples/invoices/INV-ST-1042-Sharma-Traders.pdf` | Intra-state purchase, CGST+SGST, vendor 37AABCS1234Z1Z5, buyer Example Traders 37AACTE1234F1Z5 |
| `samples/invoices/INV-RK-88-Ravi-Kirana.pdf` | Inter-state IGST 18%, Karnataka vendor |
| `samples/invoices/INV-ST-1042-duplicate.pdf` | Same number as ST/1042 — exception / duplicate check |
| `samples/bank/HDFC-50200011223344-Apr-2026.pdf` | April 2026 HDFC statement with NEFT, UPI, GST payment, unmatched cash/UPI |

In the UI: Work → pick a job (now grouped by GST, TDS, Audit, …) → upload PDFs → Run. Extract invoices and bank statement also write Excel. Master accounts workbook and Tally import reuse those registers.

## Cases

See `cases/staff-flows.md`.
