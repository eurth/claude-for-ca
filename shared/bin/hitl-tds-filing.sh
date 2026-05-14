#!/usr/bin/env bash
# hitl-tds-filing.sh
# PreToolUse hook for TRACES / TDS portal filing MCP tools.
# Returns permissionDecision: "ask" with TDS-specific HITL checklist.

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"
TOOL_INPUT="$(cat)"

FORM=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
tool = data.get('tool_name', '')
form = inp.get('form', inp.get('form_type', inp.get('return_form', '')))
if not form:
    for f in ['24Q','26Q','27Q','27EQ','27C']:
        if f.lower() in tool.lower():
            form = f
            break
print(form or 'TDS/TCS Return')
" 2>/dev/null || echo "TDS/TCS Return")

QUARTER=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('quarter', inp.get('qtr', inp.get('period', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

FY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('financial_year', inp.get('fy', inp.get('fiscal_year', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

TAN=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('tan', inp.get('TAN', inp.get('deductor_tan', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

TOTAL_TDS=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
amt = inp.get('total_tds', inp.get('total_tax_deducted', inp.get('amount', 0)))
if isinstance(amt, (int, float)) and amt > 0:
    print(f'Rs.{amt:,.0f}')
else:
    print('(verify in return)')
" 2>/dev/null || echo "(verify in return)")

PAN_ERRORS=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('pan_errors', inp.get('invalid_pan_count', 0)))
" 2>/dev/null || echo "0")

CHALLAN_COUNT=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('challan_count', inp.get('num_challans', '(verify)')))
" 2>/dev/null || echo "(verify)")

CHECKLIST="TDS/TCS FILING — HUMAN APPROVAL REQUIRED

Form      : $FORM
TAN       : $TAN
Quarter   : $QUARTER | FY: $FY
Total TDS : $TOTAL_TDS
Challans  : $CHALLAN_COUNT
PAN Errors: $PAN_ERRORS

Before approving, verify ALL of the following:

  [ ] All challans are correctly mapped to deductees
  [ ] PAN/name mismatches are zero (or explained/corrected)
  [ ] Section codes are correct for each deduction
  [ ] Late deduction / short deduction identified and interest calculated
  [ ] Form 15G/15H declarations matched — no TDS on exempt recipients
  [ ] Threshold limits applied correctly per section
  [ ] Client / employer has signed off on the return figures

Approve to proceed with filing on TRACES.
Deny to abort — fix errors before filing."

python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'ask',
        'permissionDecisionReason': sys.argv[1]
    }
}))" "$CHECKLIST"
