# Claude for CA — by Eurth / PracticeAI

> Claude AI Skills for Indian Chartered Accountants & Audit Firms

Built by **[Eurth](https://eurth.in)** | Designed for **PracticeAI** | Alpha design partner: **Gorantla Associates (CA Butchi Babu)**

---

## What This Is

`claude-for-ca` is an open-source collection of Claude AI plugins, skills, and managed agents purpose-built for Indian CA firms. It works with:

- **Claude for Work** (Anthropic Teams / Enterprise)
- **Claude Code** (VS Code / terminal)
- **Claude Managed Agents API** (headless, your own orchestrator — the PracticeAI path)

Every skill is a markdown file. Zero build step. Drop it into Claude and it works.

---

## Plugin Directory

| Plugin | What It Does |
|---|---|
| `gst-compliance` | GST return review, ITC reconciliation, notice triage, due-date watcher |
| `income-tax` | ITR cross-check, AO notice analysis, advance tax tracker |
| `tds-compliance` | TDS default detection, 26AS vs books reconciliation |
| `audit` | CARO checklist driver, audit risk matrix, internal audit workpapers |
| `mca-secretarial` | ROC filing tracker, board resolution drafter |
| `client-onboarding` | Engagement letter drafter, fee quote generator |
| `cold-start-interview` | One-time interview that writes your firm's `CLAUDE.md` profile |
| `managed-agent-cookbooks` | Scheduled agents: GST due-date watcher, TDS watcher, ROC watcher |
| `mcp-connectors` | Tally ODBC bridge, GST portal MCP wrapper |

---

## Quick Start

### Option 1 — Claude Code (Recommended for CA Butchi Babu's team)
```bash
git clone https://github.com/eurth/claude-for-ca
cd claude-for-ca

# Run the cold-start interview first — it writes your firm's CLAUDE.md
claude "Run the cold-start interview in cold-start-interview/skills/interview.SKILL.md"

# Then install any plugin
claude install plugin ./gst-compliance
```

### Option 2 — Manual Skill Use
Open any `SKILL.md` file, copy the prompt, paste into Claude with your data.

### Option 3 — ZIP Share
Download ZIP from GitHub → share with your team → they use skills directly in Claude.

---

## The Practice Profile (`CLAUDE.md`)

The `cold-start-interview` skill writes a `CLAUDE.md` for your firm. Every skill reads this file. It contains:

- Firm name, partners, client segments
- Primary jurisdiction, GST regime type
- Audit types handled
- Software stack (Tally, Excel, Zoho, etc.)
- Escalation rules
- House style (language, tone, bilingual needs)

This is the personalization layer. A `gst-compliance:review` for a Mumbai Big4 team runs differently than for Gorantla Associates, Vijayawada.

---

## MCP Connectors (Moat Layer)

| Connector | Status | What It Gives Claude |
|---|---|---|
| Tally ERP (ODBC) | ✅ Built | Trial balance, ledger dumps, voucher data |
| GST Portal | ✅ Built | GSTR-2A/2B, notice downloads |
| Google Drive | Config only | Client document folders, working papers |
| Gmail | Config only | Client communication, notice receipts |
| TRACES | Roadmap | 26AS, Form 16, TDS defaults |
| MCA21 | Roadmap | ROC filing status, charge registry |

> **Note:** Tally MCP connector and GST portal scraper are open-sourced here as reference implementations. Production hardened versions with auth, retry, and multi-client support are available via PracticeAI.

---

## Business Model

This repo is **Apache-2.0 open source**. Eurth monetizes via:

1. **PracticeAI SaaS** — hosted managed-agent deployment for CA firms
2. **Tally MCP connector** — production version (proprietary)
3. **GST/TRACES connector** — production version (proprietary)
4. **Cold-start customization** — done-for-you firm onboarding service

The open repo is the lead magnet. CA firms find it, try it, then upgrade to PracticeAI hosted.

---

## Credits

Built by **Eurth** | Conceptualized with **CA Butchi Babu, Gorantla Associates** as alpha design partner.

Inspired by the `claude-for-legal` architecture.

---

## License

Apache 2.0 — free to use, fork, and deploy. Attribution appreciated.
