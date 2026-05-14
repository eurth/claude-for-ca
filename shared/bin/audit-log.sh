#!/usr/bin/env bash
# audit-log.sh
# PostToolUse async hook — appends every MCP tool call to the append-only audit trail.
# Runs in the background (async: true) so it does not block Claude's response.

set -euo pipefail

AUDIT_DIR="${CLAUDE_PLUGIN_DATA}/claude-for-ca"
AUDIT_FILE="$AUDIT_DIR/audit_trail.jsonl"
TOOL_INPUT="$(cat)"

# Ensure the audit directory exists
mkdir -p "$AUDIT_DIR"

# Build the audit record
python3 - <<'PYEOF' "$TOOL_INPUT" "$AUDIT_FILE"
import sys, json, datetime, os, hashlib

raw_input = sys.argv[1]
audit_file = sys.argv[2]

try:
    data = json.loads(raw_input)
except json.JSONDecodeError:
    data = {}

tool_name = data.get('tool_name', 'unknown')
tool_input = data.get('tool_input', {})
tool_response = data.get('tool_response', {})
session_id = os.environ.get('CLAUDE_SESSION_ID', 'unknown')
user_id = os.environ.get('CLAUDE_USER_ID', 'unknown')

# Derive a safe input summary (no PII beyond what the tool itself contains)
input_keys = list(tool_input.keys())[:6] if isinstance(tool_input, dict) else []
input_summary = {k: str(tool_input[k])[:80] for k in input_keys}

# Detect if this was a portal filing or Tally write (higher severity)
severity = 'info'
for keyword in ['submit', 'file', 'create', 'write', 'modify', 'delete', 'post', 'amend', 'sign', 'upload']:
    if keyword in tool_name.lower():
        severity = 'high'
        break

# Extract amount if present
amount = None
for amt_key in ['amount', 'Amount', 'total_tax', 'tax_liability', 'total_debit', 'total_tds']:
    if isinstance(tool_input, dict) and amt_key in tool_input:
        try:
            amount = float(tool_input[amt_key])
            break
        except (TypeError, ValueError):
            pass

# Extract client identifier
client_id = None
for id_key in ['gstin', 'GSTIN', 'pan', 'PAN', 'cin', 'CIN', 'tan', 'TAN', 'client_id']:
    if isinstance(tool_input, dict) and id_key in tool_input:
        client_id = str(tool_input[id_key])
        break

record = {
    'ts': datetime.datetime.utcnow().isoformat() + 'Z',
    'session_id': session_id,
    'user_id': user_id,
    'tool': tool_name,
    'severity': severity,
    'input_summary': input_summary,
    'client_id': client_id,
    'amount': amount,
    'success': 'error' not in str(tool_response).lower()
}

with open(audit_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(record, ensure_ascii=False) + '\n')
PYEOF
