#!/usr/bin/env bash
# hitl-gst-filing.sh
# PreToolUse hook for GST portal filing/submission MCP tools.
# Reads tool input JSON from stdin, queries memory bank for client context,
# returns permissionDecision: "ask" with a structured HITL checklist.
# Exit 0 = pass control to Claude Code permission dialog.
# Exit 2 = hard block (not used here — we always ask).

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"
TOOL_INPUT="$(cat)"

# Extract fields from tool input JSON
GSTIN=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('gstin', inp.get('GSTIN', inp.get('taxpayer_gstin', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

PERIOD=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('period', inp.get('return_period', inp.get('tax_period', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

RETURN_TYPE=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tool = data.get('tool_name', '')
inp = data.get('tool_input', {})
rt = inp.get('return_type', inp.get('form_type', ''))
if not rt:
    for kw in ['gstr1','gstr3b','gstr9c','gstr9','gstr7','gstr8','pmt06']:
        if kw in tool.lower():
            rt = kw.upper()
            break
print(rt or 'GST Return')
" 2>/dev/null || echo "GST Return")

TAX_LIABILITY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
amt = inp.get('tax_liability', inp.get('total_tax', inp.get('amount', 0)))
if isinstance(amt, (int, float)) and amt > 0:
    print(f'Rs.{amt:,.0f}')
else:
    print('(verify in return)')
" 2>/dev/null || echo "(verify in return)")

# Look up client name from memory bank (best-effort)
CLIENT_NAME="Unknown Client"
if [ -f "$DB" ] && command -v sqlite3 &>/dev/null; then
    CLIENT_NAME=$(sqlite3 "$DB" "SELECT name FROM clients WHERE gstin='$GSTIN' LIMIT 1;" 2>/dev/null || echo "")
    if [ -z "$CLIENT_NAME" ]; then
        CLIENT_NAME="Client (GSTIN: $GSTIN)"
    fi
fi

# Build the HITL checklist message
CHECKLIST="GST FILING — HUMAN APPROVAL REQUIRED

Return    : $RETURN_TYPE
Client    : $CLIENT_NAME
GSTIN     : $GSTIN
Period    : $PERIOD
Tax Amt   : $TAX_LIABILITY

Before approving, verify ALL of the following:

  [ ] GSTR-1 (outward supplies) is filed for this period
  [ ] ITC reconciled with GSTR-2B (mismatches investigated)
  [ ] Rule 42/43 pro-rata reversals applied for mixed supplies
  [ ] Cash/credit ledger balance is sufficient to pay tax
  [ ] NIL / exempt supplies correctly classified
  [ ] Late fee / interest calculated if applicable
  [ ] Client has explicitly authorised this filing

Approve to proceed with filing.
Deny to abort — review the return manually first."

# Emit the hook output JSON
python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'ask',
        'permissionDecisionReason': sys.argv[1]
    }
}))" "$CHECKLIST"
