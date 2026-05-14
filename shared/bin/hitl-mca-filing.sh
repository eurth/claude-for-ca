#!/usr/bin/env bash
# hitl-mca-filing.sh
# PreToolUse hook for MCA21 / ROC portal filing MCP tools.

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"
TOOL_INPUT="$(cat)"

FORM=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
tool = data.get('tool_name', '')
form = inp.get('form', inp.get('form_type', inp.get('eform', '')))
if not form:
    for f in ['AOC4','MGT7','DIR3KYC','INC22','CHG1','DPT3','MSME1','BEN2','PAS3']:
        if f.lower().replace('-','') in tool.lower().replace('-','') or f.lower() in tool.lower():
            form = f
            break
print(form or 'MCA/ROC Form')
" 2>/dev/null || echo "MCA/ROC Form")

CIN=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('cin', inp.get('CIN', inp.get('company_cin', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

COMPANY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('company_name', inp.get('company', inp.get('name', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

FY=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
print(inp.get('financial_year', inp.get('fy', inp.get('year', 'UNKNOWN'))))
" 2>/dev/null || echo "UNKNOWN")

SIGNATORIES=$(echo "$TOOL_INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
inp = data.get('tool_input', {})
sigs = inp.get('signatories', inp.get('directors', inp.get('authorized_signatories', [])))
if isinstance(sigs, list) and sigs:
    print(', '.join(str(s) for s in sigs[:3]))
else:
    print('(verify in form)')
" 2>/dev/null || echo "(verify in form)")

CHECKLIST="MCA / ROC FILING — HUMAN APPROVAL REQUIRED

Form       : $FORM
Company    : $COMPANY
CIN        : $CIN
Period/FY  : $FY
Signatories: $SIGNATORIES

Before approving, verify ALL of the following:

  [ ] Financial statements / annexures are board-approved
  [ ] DSC (Digital Signature Certificate) of authorized signatory is valid
  [ ] All DIN/PAN details of directors are correct
  [ ] Filing fees calculated and payment challan ready
  [ ] Previous filings for this company are current (no pending dues)
  [ ] SRN of any linked/predecessor form noted
  [ ] Board resolution / AGM resolution authorising filing is in place
  [ ] Late filing fee / additional fee calculated if deadline has passed

Approve to proceed with MCA21 filing.
Deny to abort — complete board approvals before filing."

python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'ask',
        'permissionDecisionReason': sys.argv[1]
    }
}))" "$CHECKLIST"
