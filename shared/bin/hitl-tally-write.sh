#!/usr/bin/env bash
# hitl-tally-write.sh
# PreToolUse hook for Tally MCP write operations (create/modify/delete vouchers, entries).
# Tally writes are NOT easily reversible — requires explicit CA approval.

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"
THRESHOLD="${CLAUDE_PLUGIN_OPTION_HITL_AMOUNT_THRESHOLD:-100000}"
TOOL_INPUT="$(cat)"

TOOL_NAME=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_name', 'mcp__tally__unknown'))
" 2>/dev/null || echo "mcp__tally__unknown")

VOUCHER_TYPE=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('voucher_type', inp.get('VoucherType', inp.get('type', 'Voucher'))))
" 2>/dev/null || echo "Voucher")

VOUCHER_COUNT=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
vouchers = inp.get('vouchers', inp.get('entries', []))
if isinstance(vouchers, list):
    print(len(vouchers))
else:
    print(1)
" 2>/dev/null || echo "1")

TOTAL_DEBIT=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
amt = inp.get('total_debit', inp.get('amount', inp.get('Amount', 0)))
if isinstance(amt, (int, float)) and amt > 0:
    print(f'Rs.{amt:,.0f}')
else:
    print('(calculate before approving)')
" 2>/dev/null || echo "(calculate before approving)")

VOUCHER_DATE=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('date', inp.get('Date', inp.get('voucher_date', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

COMPANY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('company', inp.get('Company', inp.get('company_name', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

CHECKLIST="TALLY WRITE OPERATION — HUMAN APPROVAL REQUIRED

⚠  THIS ACTION MODIFIES ACCOUNTING DATA AND IS NOT EASILY REVERSIBLE

Tool         : $TOOL_NAME
Company      : $COMPANY
Voucher Type : $VOUCHER_TYPE
Voucher Count: $VOUCHER_COUNT
Total Debit  : $TOTAL_DEBIT
Date         : $VOUCHER_DATE
Threshold    : Rs.$THRESHOLD (configured limit)

Before approving, verify ALL of the following:

  [ ] Voucher type and narration are correct
  [ ] Debit/credit amounts foot correctly
  [ ] Ledger heads map to the correct groups
  [ ] Date is within the correct accounting period
  [ ] Cost centre / project tagging is correct (if applicable)
  [ ] This entry is not a duplicate of an existing voucher
  [ ] Client / employer has reviewed the journal entry

Approve to post entries to Tally.
Deny to abort — review the draft entries in Excel first."

python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'ask',
        'permissionDecisionReason': sys.argv[1]
    }
}))" "$CHECKLIST"
