# Setup Guide — Claude Desktop for Indian CA Firms

## Who is this guide for?
This guide is for CA firm staff who want to use AI assistance for daily compliance work. **No technical background required.** You do not need to know programming.

---

## WHAT YOU GET AFTER SETUP

Each "Project" in Claude Desktop becomes a specialist assistant:
- **GST Compliance** — GSTR-1/3B/9 review, ITC reconciliation, notice drafting
- **Income Tax + TDS** — ITR selection, advance tax, 26AS reconciliation, notice response
- **Audit & Assurance** — CARO 2020 checklists, bank audit NPA norms, audit workpapers
- **MCA + TP + FEMA** — ROC filings, board resolutions, transfer pricing, FDI reporting
- **Advisory + Payroll** — Old/new regime comparison, PF/ESIC calculations, MSME rules
- **Client & Firm Management** — KYC checklists, engagement letters, fee reminders

---

## STEP 1 — WHAT YOU NEED

### Claude Plan Required
- **Individual use**: Claude Pro (USD 20/month) — 1 user
- **Firm with 2–5 staff**: Claude Team (USD 30/user/month) — best option
- Sign up at: [claude.ai](https://claude.ai)

### Computer Requirements
- Windows 10/11 or macOS — any modern laptop or desktop is fine
- Internet connection
- 200 MB free disk space

---

## STEP 2 — INSTALL CLAUDE DESKTOP

1. Go to **claude.ai/download** in your browser
2. Download the installer for your operating system (Windows or Mac)
3. Run the installer — it works like any normal software installation
4. Log in with the same Anthropic/Claude account you created in Step 1

---

## STEP 3 — CREATE YOUR FIRST PROJECT

1. Open Claude Desktop
2. On the left sidebar, click **"+" (New Project)**
3. Give it a name — e.g. **"GST Compliance"**
4. Click **"Set project instructions"** (or "Add instructions")
5. Open the file [01-gst-compliance.md](01-gst-compliance.md) from this folder
6. Copy everything between the `━━━━━` separator lines
7. Paste it into the instructions box
8. Click **Save**
9. Repeat for each domain using files 02 through 06

**That's it.** You can now chat with your GST assistant by clicking the project and typing naturally.

---

## STEP 4 — HOW TO TALK TO THE ASSISTANT

No commands needed. Just describe what you need in plain English:

> "My client Rajesh Traders received a DRC-01 notice from GST department for Rs.3.5 lakh mismatch in GSTR-3B for FY 2022-23. Help me draft a reply."

> "Give me the CARO checklist for a private limited company with turnover Rs.12 Cr."

> "Calculate advance tax for a doctor with Rs.22 lakh income — all 4 instalments."

> "What ROC forms are due after the AGM was held on 20 September?"

You can paste notice text, financial data, or any document — the assistant will analyse it.

---

## STEP 5 (OPTIONAL) — CONNECT TALLY FOR LIVE DATA

This step lets the assistant directly read your Tally data — trial balance, ledger reports, stock reports.

**Requirements**: Tally Prime or Tally ERP 9 running on the same computer or on your office network.

### How to Connect Tally

1. **Install Python** (free): Go to [python.org/downloads](https://python.org/downloads) → Download Python 3.11 or 3.12 → Install with "Add to PATH" checked
2. **Install the connector**: Open Command Prompt (Start → type `cmd` → Enter) and run:
   ```
   pip install fastmcp requests
   ```
3. **Copy the Tally MCP server file** — the file is in `mcp-connectors/tally/tally_mcp_wrapper.py` in this project
4. **Find the Claude Desktop config file**:
   - Windows: `C:\Users\[YourName]\AppData\Roaming\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
5. **Open that config file** in Notepad and add the following (replace `C:\PATH\TO` with your actual path):

```json
{
  "mcpServers": {
    "tally": {
      "command": "python",
      "args": ["C:\\PATH\\TO\\mcp-connectors\\tally\\tally_mcp_wrapper.py"],
      "env": {
        "TALLY_URL": "http://localhost:9000"
      }
    }
  }
}
```

6. **Start Tally** with ODBC enabled (Tally → Gateway of Tally → Connect → set port 9000)
7. **Restart Claude Desktop** — you will see a plug icon (🔌) in the chat indicating Tally is connected

After this, you can ask: *"Get the trial balance from Tally for April 2025"* and the assistant will fetch it directly.

> **Note**: The Tally connector is READ-ONLY by default. Creating vouchers requires explicit CA approval each time — you will be asked to confirm before anything is posted.

---

## STEP 6 (OPTIONAL) — UPLOAD REFERENCE DOCUMENTS

In any Project, you can upload files (PDFs, Excel, Word) that Claude will use as reference:
- Upload your client's audited financial statements
- Upload a GST notice (PDF) to get a detailed analysis
- Upload a bank statement for reconciliation help
- Upload your firm's standard engagement letter template

Click the paperclip icon in the chat to attach files.

---

## ARCHITECTURE — HOW IT ALL WORKS

```
Your Question (plain English)
         ↓
Claude Desktop Project
(with domain system prompt)
         ↓
Claude AI (Anthropic servers)
  ├─ Analyses your question using the knowledge in the project instructions
  ├─ Applies Indian tax law, ICAI standards, and compliance rules
  └─ Optionally reads live Tally data via MCP connector (if connected)
         ↓
Response: Draft notice reply / Calculation / Checklist / Analysis
         ↓
CA reviews, approves, and files / sends
```

The AI never directly files anything. It drafts and analyses. You review and act.

---

## PRIVACY & SECURITY

- Claude Desktop processes your queries on Anthropic's servers (USA-based, SOC 2 compliant)
- Do NOT paste client PAN numbers, Aadhaar numbers, or bank account numbers if you have concerns
- For sensitive work: Use generic descriptions ("my client, a manufacturing company...") instead of actual names
- Claude Pro/Teams: Your conversations are not used to train Anthropic's models (as per Anthropic's policy)
- All responses are drafts — nothing is transmitted to government portals unless you copy-paste and file manually

---

## WHICH FILE DOES WHAT

| File | Use For |
|------|---------|
| [01-gst-compliance.md](01-gst-compliance.md) | GST Project instructions |
| [02-income-tax-tds.md](02-income-tax-tds.md) | Income Tax + TDS Project instructions |
| [03-audit-assurance.md](03-audit-assurance.md) | Audit Project instructions |
| [04-mca-tp-fema.md](04-mca-tp-fema.md) | MCA + TP + FEMA Project instructions |
| [05-advisory-payroll.md](05-advisory-payroll.md) | Advisory + Payroll Project instructions |
| [06-client-firm-management.md](06-client-firm-management.md) | Client onboarding + Firm management Project instructions |
| [07-opensource-alternatives.md](07-opensource-alternatives.md) | Free / open-source options if you don't want Claude |
| This file | You're reading it |

---

## TROUBLESHOOTING

**"Claude doesn't know my firm name / client details"**
→ Either tell it in the chat ("my firm is ABC & Associates") or add your firm profile to the Project instructions

**"The answer is too generic"**
→ Give more context: paste the actual notice, mention the specific section, give the numbers

**"The Tally connector isn't working"**
→ Check: (a) Tally is running with ODBC enabled, (b) port 9000 is not blocked by firewall, (c) Python is installed and `fastmcp` is installed, (d) Claude Desktop was restarted after editing config

**"I want to add more details to the system prompt"**
→ You can edit the Project instructions at any time — just click the project → Edit instructions → add your firm's specific details, common client types, or preferred formats
