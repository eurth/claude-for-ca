# Tally MCP Connector

Bridges Tally Prime (via ODBC) to the MCP (Model Context Protocol) interface so Claude can directly query trial balances, ledgers, and voucher data.

## Prerequisites
- Tally Prime 3.x or higher with ODBC enabled
- Python 3.10+
- `pyodbc` library
- Tally ODBC driver installed (comes with Tally Prime)

## Setup

### 1. Enable ODBC in Tally Prime
- Open Tally Prime → Gateway of Tally → F12 Configure → Advanced Configuration
- Set **Enable ODBC Server**: Yes
- ODBC Port: 9000 (default)
- Restart Tally

### 2. Install Dependencies
```bash
pip install pyodbc mcp fastapi uvicorn
```

### 3. Configure Connection
Edit `tally_mcp_wrapper.py` — set:
```python
TALLY_DSN = "TallyODBC64_9000"   # matches your Tally ODBC DSN name
TALLY_COMPANY = "Your Company Name"  # as it appears in Tally
```

### 4. Run the MCP Server
```bash
python tally_mcp_wrapper.py
```
Server starts at `http://localhost:8001`

### 5. Register in .mcp.json
```json
{
  "tally": {
    "url": "http://localhost:8001",
    "description": "Tally Prime ODBC connector — trial balance, ledgers, vouchers"
  }
}
```

## Available Tools

| Tool | Description | Parameters |
|---|---|---|
| `get_trial_balance` | Fetch trial balance for a company/period | company, from_date, to_date |
| `get_ledger` | Fetch ledger entries for a specific account | company, ledger_name, from_date, to_date |
| `get_vouchers` | Fetch voucher list by type and period | company, voucher_type, from_date, to_date |
| `get_gst_summary` | Fetch GST summary (outward/inward) | company, period |
| `get_tds_summary` | Fetch TDS deduction summary | company, period |
| `search_party` | Search for a party (customer/supplier) by name or GSTIN | query |
