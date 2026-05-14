#!/usr/bin/env bash
# hitl-itr-filing.sh
# PreToolUse hook for Income Tax / e-filing portal submission MCP tools.

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"
TOOL_INPUT="$(cat)"

PAN=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('pan', inp.get('PAN', inp.get('taxpayer_pan', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

AY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('assessment_year', inp.get('ay', inp.get('AY', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

ITR_FORM=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
tool = data.get('tool_name', '')
form = inp.get('itr_form', inp.get('form', inp.get('return_form', '')))
if not form:
    for f in ['ITR1','ITR2','ITR3','ITR4','ITR5','ITR6','ITR7']:
        if f.lower() in tool.lower():
            form = f
            break
print(form or 'ITR')
" 2>/dev/null || echo "ITR")

TAX_PAYABLE=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
amt = inp.get('tax_payable', inp.get('self_assessment_tax', inp.get('total_tax', 0)))
if isinstance(amt, (int, float)):
    if amt > 0:
        print(f'Rs.{amt:,.0f} (payable)')
    elif amt < 0:
        print(f'Rs.{abs(amt):,.0f} (refund due)')
    else:
        print('Nil')
else:
    print('(verify in computation)')
" 2>/dev/null || echo "(verify in computation)")

CLIENT_NAME="Unknown Client"
if [ -f "$DB" ] && command -v sqlite3 &>/dev/null && [ "$PAN" != "UNKNOWN" ]; then
    CLIENT_NAME=$(sqlite3 "$DB" "SELECT name FROM clients WHERE pan='$PAN' LIMIT 1;" 2>/dev/null || echo "")
    if [ -z "$CLIENT_NAME" ]; then
        CLIENT_NAME="Client (PAN: $PAN)"
    fi
fi

CHECKLIST="ITR FILING — HUMAN APPROVAL REQUIRED

Form          : $ITR_FORM
Client        : $CLIENT_NAME
PAN           : $PAN
Assessment Yr : $AY
Tax Position  : $TAX_PAYABLE

Before approving, verify ALL of the following:

  [ ] Gross total income matches Form 26AS / AIS / TIS
  [ ] All TDS credits (26AS) are reflected and matched
  [ ] Advance tax and self-assessment tax challans are updated
  [ ] Capital gains (if any) are computed with correct cost/date
  [ ] Foreign income / DTAA relief computed correctly (if applicable)
  [ ] Deductions under Chapter VI-A are supported by proofs
  [ ] Carry-forward losses are correctly brought forward
  [ ] Client has signed the verification (ITR-V) or EVC is set up
  [ ] Refund bank account is pre-validated on portal

Approve to submit ITR on the e-filing portal.
Deny to abort — address any open items first."

python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'ask',
        'permissionDecisionReason': sys.argv[1]
    }
}))" "$CHECKLIST"
