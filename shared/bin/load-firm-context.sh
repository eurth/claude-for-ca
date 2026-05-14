#!/usr/bin/env bash
# load-firm-context.sh
# SessionStart hook — reads practice.db and emits firm context + integrity reminder
# as additionalContext so every Claude session starts with firm awareness.

set -euo pipefail

DB="${MEMORY_BANK_DB:-${CLAUDE_PLUGIN_DATA}/claude-for-ca/practice.db}"

# If database does not exist yet (pre-onboarding), emit a setup prompt
if [ ! -f "$DB" ]; then
    python3 -c "
import json
print(json.dumps({
    'additionalContext': '## Claude for CA — Setup Required\n\nNo firm profile found. Please run the onboarding skill first:\n\n  /cold-start:onboard-firm\n\nThis one-time interview will set up your firm profile, client registry, and compliance calendar in the local memory bank.'
}))
"
    exit 0
fi

# Query practice.db for firm context and today's due items
python3 - <<'PYEOF' "$DB"
import sys, json, sqlite3, datetime

db_path = sys.argv[1]
today = datetime.date.today()
week_end = today + datetime.timedelta(days=7)
month_end = today + datetime.timedelta(days=30)

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Firm profile
    firm = {}
    try:
        cur.execute("SELECT * FROM firm_profile LIMIT 1")
        row = cur.fetchone()
        if row:
            firm = dict(row)
    except sqlite3.OperationalError:
        pass

    # Client count
    client_count = 0
    try:
        cur.execute("SELECT COUNT(*) FROM clients")
        client_count = cur.fetchone()[0]
    except sqlite3.OperationalError:
        pass

    # Due this week
    due_this_week = []
    try:
        cur.execute("""
            SELECT form_type, COUNT(*) as cnt
            FROM compliance_calendar
            WHERE due_date BETWEEN ? AND ? AND status NOT IN ('filed','completed','nil')
            GROUP BY form_type
            ORDER BY cnt DESC
        """, (today.isoformat(), week_end.isoformat()))
        for row in cur.fetchall():
            due_this_week.append(f"{row['form_type']} ({row['cnt']})")
    except sqlite3.OperationalError:
        pass

    # Pending notices
    pending_notices = []
    try:
        cur.execute("""
            SELECT c.name, n.section, n.notice_ref
            FROM notices n
            LEFT JOIN clients c ON n.client_id = c.client_id
            WHERE n.status IN ('received','pending','in_progress')
            ORDER BY n.due_date ASC
            LIMIT 5
        """)
        for row in cur.fetchall():
            pending_notices.append(f"{row['name']} — Section {row['section']} ({row['notice_ref']})")
    except sqlite3.OperationalError:
        pass

    # Build context block
    lines = ["## Claude for CA — Session Context"]
    lines.append("")

    if firm:
        lines.append(f"**Firm:** {firm.get('firm_name', 'N/A')}  |  **CA:** {firm.get('ca_name', 'N/A')}  |  **GSTIN:** {firm.get('firm_gstin', 'N/A')}")
        lines.append(f"**Jurisdiction:** {firm.get('jurisdiction', 'N/A')}  |  **Tally DSN:** {firm.get('tally_dsn', 'not configured')}")
    else:
        lines.append("**Firm profile not yet configured.** Run `/cold-start:onboard-firm` to complete setup.")

    lines.append(f"**Active clients:** {client_count}")

    if due_this_week:
        lines.append(f"**Due this week (7 days):** {', '.join(due_this_week)}")
    else:
        lines.append("**Due this week:** Nothing due (or calendar not yet populated)")

    if pending_notices:
        lines.append(f"**Pending notices ({len(pending_notices)}):**")
        for notice in pending_notices:
            lines.append(f"  - {notice}")

    lines.append("")
    lines.append("---")
    lines.append("**FINANCIAL INTEGRITY RULE:** All GST / TDS / ITR / MCA filings and all Tally write operations require explicit CA approval. I will present a checklist and pause for your confirmation before taking any such action. I will never auto-file.")
    lines.append("")

    print(json.dumps({'additionalContext': '\n'.join(lines)}))
    conn.close()

except Exception as e:
    # Non-fatal — session proceeds without context if DB is unreadable
    print(json.dumps({'additionalContext': f'## Claude for CA\n\n(Memory bank unavailable: {str(e)[:100]})\n\n**INTEGRITY RULE:** All filings and Tally writes require explicit CA approval.'}))
PYEOF
