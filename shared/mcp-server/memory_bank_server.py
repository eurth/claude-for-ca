#!/usr/bin/env python3
"""
memory_bank_server.py — Offline SQLite MCP server for Claude for CA
Provides: firm profile, client registry, notice tracker,
          compliance calendar, and append-only audit trail.

Runs as a local subprocess via .mcp.json.
All data stored in ${MEMORY_BANK_DB} (default: ~/claude/plugins/data/claude-for-ca-core/practice.db).
"""

import os
import json
import sqlite3
import datetime
import sys
from pathlib import Path
from typing import Any

# ── MCP SDK ─────────────────────────────────────────────────────────────────
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types
except ImportError:
    print(
        json.dumps({
            "error": "mcp package not installed. Run: pip install mcp",
            "hint": "pip install mcp"
        }),
        file=sys.stderr
    )
    sys.exit(1)

# ── Database path ─────────────────────────────────────────────────────────────
DB_PATH = Path(
    os.environ.get(
        "MEMORY_BANK_DB",
        Path.home() / ".claude" / "plugins" / "data" / "claude-for-ca-core" / "practice.db"
    )
)

# ── Schema ────────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS firm_profile (
    id                  INTEGER PRIMARY KEY CHECK (id = 1),
    firm_name           TEXT NOT NULL,
    ca_name             TEXT NOT NULL,
    firm_gstin          TEXT,
    ca_registration_no  TEXT,
    jurisdiction        TEXT,
    tally_dsn           TEXT,
    fiscal_year_start   INTEGER DEFAULT 4,
    address             TEXT,
    phone               TEXT,
    email               TEXT,
    software_stack      TEXT,
    updated_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clients (
    client_id       TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    pan             TEXT,
    gstin           TEXT,
    tan             TEXT,
    cin             TEXT,
    entity_type     TEXT,
    constitution    TEXT,
    industry        TEXT,
    jurisdiction    TEXT,
    contact_name    TEXT,
    contact_email   TEXT,
    contact_phone   TEXT,
    tally_company   TEXT,
    notes           TEXT,
    active          INTEGER DEFAULT 1,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notices (
    notice_id       TEXT PRIMARY KEY,
    client_id       TEXT NOT NULL,
    portal          TEXT,
    section         TEXT,
    notice_ref      TEXT,
    notice_date     TEXT,
    due_date        TEXT,
    demand_amount   REAL,
    assessment_year TEXT,
    notice_type     TEXT,
    status          TEXT DEFAULT 'received',
    ai_draft_path   TEXT,
    resolution_note TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS compliance_calendar (
    task_id         TEXT PRIMARY KEY,
    client_id       TEXT,
    form_type       TEXT NOT NULL,
    period          TEXT,
    due_date        TEXT NOT NULL,
    description     TEXT,
    filed_date      TEXT,
    filed_by        TEXT,
    status          TEXT DEFAULT 'pending',
    notes           TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS audit_trail (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ts              TEXT NOT NULL,
    session_id      TEXT,
    user_id         TEXT,
    tool            TEXT NOT NULL,
    severity        TEXT DEFAULT 'info',
    client_id       TEXT,
    amount          REAL,
    input_summary   TEXT,
    success         INTEGER DEFAULT 1,
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_clients_pan ON clients(pan);
CREATE INDEX IF NOT EXISTS idx_clients_gstin ON clients(gstin);
CREATE INDEX IF NOT EXISTS idx_notices_client ON notices(client_id);
CREATE INDEX IF NOT EXISTS idx_notices_status ON notices(status);
CREATE INDEX IF NOT EXISTS idx_calendar_due ON compliance_calendar(due_date);
CREATE INDEX IF NOT EXISTS idx_calendar_client ON compliance_calendar(client_id);
CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_trail(ts);
CREATE INDEX IF NOT EXISTS idx_audit_client ON audit_trail(client_id);
"""


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def row_to_dict(row) -> dict:
    return dict(row) if row else {}


# ── MCP Server ────────────────────────────────────────────────────────────────
server = Server("memory-bank")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_firm_profile",
            description="Retrieve the CA firm's profile (name, GSTIN, partners, Tally DSN, jurisdiction).",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        types.Tool(
            name="save_firm_profile",
            description="Create or update the firm profile. Called once during onboarding.",
            inputSchema={
                "type": "object",
                "properties": {
                    "firm_name": {"type": "string"},
                    "ca_name": {"type": "string"},
                    "firm_gstin": {"type": "string"},
                    "ca_registration_no": {"type": "string"},
                    "jurisdiction": {"type": "string"},
                    "tally_dsn": {"type": "string"},
                    "fiscal_year_start": {"type": "integer"},
                    "address": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "software_stack": {"type": "string"}
                },
                "required": ["firm_name", "ca_name"]
            }
        ),
        types.Tool(
            name="get_client",
            description="Get a client's full profile by client_id, PAN, GSTIN, CIN, or TAN.",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string"},
                    "pan": {"type": "string"},
                    "gstin": {"type": "string"},
                    "cin": {"type": "string"},
                    "tan": {"type": "string"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="list_clients",
            description="List all clients, optionally filtered by entity_type, active status, or name search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string"},
                    "active_only": {"type": "boolean"},
                    "name_search": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_client",
            description="Create or update a client record. If client_id exists, it is updated.",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string"},
                    "name": {"type": "string"},
                    "pan": {"type": "string"},
                    "gstin": {"type": "string"},
                    "tan": {"type": "string"},
                    "cin": {"type": "string"},
                    "entity_type": {"type": "string"},
                    "constitution": {"type": "string"},
                    "industry": {"type": "string"},
                    "jurisdiction": {"type": "string"},
                    "contact_name": {"type": "string"},
                    "contact_email": {"type": "string"},
                    "contact_phone": {"type": "string"},
                    "tally_company": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["name"]
            }
        ),
        types.Tool(
            name="log_notice",
            description="Record a statutory notice received for a client (IT, GST, ROC, FEMA, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string"},
                    "portal": {"type": "string", "description": "income_tax | gst | mca | fema | pf_esic"},
                    "section": {"type": "string"},
                    "notice_ref": {"type": "string"},
                    "notice_date": {"type": "string"},
                    "due_date": {"type": "string"},
                    "demand_amount": {"type": "number"},
                    "assessment_year": {"type": "string"},
                    "notice_type": {"type": "string"}
                },
                "required": ["client_id", "portal", "section"]
            }
        ),
        types.Tool(
            name="update_notice_status",
            description="Update the status of a notice (received | in_progress | responded | resolved | closed).",
            inputSchema={
                "type": "object",
                "properties": {
                    "notice_id": {"type": "string"},
                    "status": {"type": "string"},
                    "resolution_note": {"type": "string"},
                    "ai_draft_path": {"type": "string"}
                },
                "required": ["notice_id", "status"]
            }
        ),
        types.Tool(
            name="list_notices",
            description="List notices, optionally filtered by client_id, status, or portal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string"},
                    "status": {"type": "string"},
                    "portal": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="log_compliance_event",
            description="Add or update a compliance task in the calendar (GST return, TDS return, ITR, ROC filing, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "client_id": {"type": "string"},
                    "form_type": {"type": "string"},
                    "period": {"type": "string"},
                    "due_date": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["form_type", "due_date"]
            }
        ),
        types.Tool(
            name="mark_filing_complete",
            description="Mark a compliance calendar task as filed/completed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "filed_date": {"type": "string"},
                    "filed_by": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["task_id"]
            }
        ),
        types.Tool(
            name="get_due_dates",
            description="Get upcoming compliance due dates within the next N days (default 30).",
            inputSchema={
                "type": "object",
                "properties": {
                    "days_ahead": {"type": "integer"},
                    "client_id": {"type": "string"},
                    "include_filed": {"type": "boolean"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="query_audit_trail",
            description="Query the audit trail log for a client, date range, or tool.",
            inputSchema={
                "type": "object",
                "properties": {
                    "client_id": {"type": "string"},
                    "from_date": {"type": "string"},
                    "to_date": {"type": "string"},
                    "tool_prefix": {"type": "string"},
                    "severity": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="log_audit_entry",
            description="Append a record to the audit trail. Called by audit-log.sh automatically after each MCP call.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "tool": {"type": "string"},
                    "severity": {"type": "string"},
                    "client_id": {"type": "string"},
                    "amount": {"type": "number"},
                    "input_summary": {"type": "string"},
                    "success": {"type": "boolean"},
                    "notes": {"type": "string"}
                },
                "required": ["tool"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    conn = get_db()
    try:
        result = _dispatch(conn, name, arguments)
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    finally:
        conn.close()


def _dispatch(conn: sqlite3.Connection, name: str, args: dict) -> Any:
    match name:
        case "get_firm_profile":
            return _get_firm_profile(conn)
        case "save_firm_profile":
            return _save_firm_profile(conn, args)
        case "get_client":
            return _get_client(conn, args)
        case "list_clients":
            return _list_clients(conn, args)
        case "save_client":
            return _save_client(conn, args)
        case "log_notice":
            return _log_notice(conn, args)
        case "update_notice_status":
            return _update_notice_status(conn, args)
        case "list_notices":
            return _list_notices(conn, args)
        case "log_compliance_event":
            return _log_compliance_event(conn, args)
        case "mark_filing_complete":
            return _mark_filing_complete(conn, args)
        case "get_due_dates":
            return _get_due_dates(conn, args)
        case "query_audit_trail":
            return _query_audit_trail(conn, args)
        case "log_audit_entry":
            return _log_audit_entry(conn, args)
        case _:
            return {"error": f"Unknown tool: {name}"}


# ── Tool implementations ─────────────────────────────────────────────────────

def _get_firm_profile(conn):
    row = conn.execute("SELECT * FROM firm_profile WHERE id = 1").fetchone()
    if not row:
        return {"status": "not_configured", "message": "Firm profile not yet set up. Run /cold-start:onboard-firm"}
    return {"status": "ok", "firm": row_to_dict(row)}


def _save_firm_profile(conn, args):
    ts = now_iso()
    conn.execute("""
        INSERT INTO firm_profile (id, firm_name, ca_name, firm_gstin, ca_registration_no,
            jurisdiction, tally_dsn, fiscal_year_start, address, phone, email,
            software_stack, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            firm_name=excluded.firm_name, ca_name=excluded.ca_name,
            firm_gstin=excluded.firm_gstin, ca_registration_no=excluded.ca_registration_no,
            jurisdiction=excluded.jurisdiction, tally_dsn=excluded.tally_dsn,
            fiscal_year_start=excluded.fiscal_year_start, address=excluded.address,
            phone=excluded.phone, email=excluded.email,
            software_stack=excluded.software_stack, updated_at=excluded.updated_at
    """, (
        args.get("firm_name"), args.get("ca_name"), args.get("firm_gstin"),
        args.get("ca_registration_no"), args.get("jurisdiction"),
        args.get("tally_dsn", ""), args.get("fiscal_year_start", 4),
        args.get("address", ""), args.get("phone", ""), args.get("email", ""),
        args.get("software_stack", ""), ts
    ))
    conn.commit()
    return {"status": "ok", "message": "Firm profile saved."}


def _get_client(conn, args):
    for col in ("client_id", "pan", "gstin", "cin", "tan"):
        val = args.get(col)
        if val:
            row = conn.execute(
                f"SELECT * FROM clients WHERE {col} = ? LIMIT 1", (val,)
            ).fetchone()
            if row:
                return {"status": "ok", "client": row_to_dict(row)}
    return {"status": "not_found", "message": "No client found with the provided identifiers."}


def _list_clients(conn, args):
    q = "SELECT * FROM clients WHERE 1=1"
    params = []
    if args.get("active_only", True):
        q += " AND active = 1"
    if args.get("entity_type"):
        q += " AND entity_type = ?"
        params.append(args["entity_type"])
    if args.get("name_search"):
        q += " AND name LIKE ?"
        params.append(f"%{args['name_search']}%")
    q += " ORDER BY name"
    limit = min(int(args.get("limit", 100)), 500)
    q += f" LIMIT {limit}"
    rows = conn.execute(q, params).fetchall()
    return {"status": "ok", "count": len(rows), "clients": [row_to_dict(r) for r in rows]}


def _save_client(conn, args):
    import uuid
    ts = now_iso()
    client_id = args.get("client_id") or f"c_{uuid.uuid4().hex[:8]}"
    existing = conn.execute(
        "SELECT client_id FROM clients WHERE client_id = ?", (client_id,)
    ).fetchone()
    if existing:
        conn.execute("""
            UPDATE clients SET name=?, pan=?, gstin=?, tan=?, cin=?,
                entity_type=?, constitution=?, industry=?, jurisdiction=?,
                contact_name=?, contact_email=?, contact_phone=?,
                tally_company=?, notes=?, updated_at=?
            WHERE client_id=?
        """, (
            args.get("name"), args.get("pan"), args.get("gstin"),
            args.get("tan"), args.get("cin"), args.get("entity_type"),
            args.get("constitution"), args.get("industry"), args.get("jurisdiction"),
            args.get("contact_name"), args.get("contact_email"),
            args.get("contact_phone"), args.get("tally_company"),
            args.get("notes"), ts, client_id
        ))
    else:
        conn.execute("""
            INSERT INTO clients (client_id, name, pan, gstin, tan, cin,
                entity_type, constitution, industry, jurisdiction,
                contact_name, contact_email, contact_phone,
                tally_company, notes, active, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1,?,?)
        """, (
            client_id, args.get("name"), args.get("pan"), args.get("gstin"),
            args.get("tan"), args.get("cin"), args.get("entity_type"),
            args.get("constitution"), args.get("industry"), args.get("jurisdiction"),
            args.get("contact_name"), args.get("contact_email"),
            args.get("contact_phone"), args.get("tally_company"),
            args.get("notes"), ts, ts
        ))
    conn.commit()
    return {"status": "ok", "client_id": client_id}


def _log_notice(conn, args):
    import uuid
    ts = now_iso()
    notice_id = f"n_{uuid.uuid4().hex[:10]}"
    conn.execute("""
        INSERT INTO notices (notice_id, client_id, portal, section, notice_ref,
            notice_date, due_date, demand_amount, assessment_year, notice_type,
            status, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,'received',?,?)
    """, (
        notice_id, args["client_id"], args["portal"], args["section"],
        args.get("notice_ref", ""), args.get("notice_date"), args.get("due_date"),
        args.get("demand_amount"), args.get("assessment_year"),
        args.get("notice_type", ""), ts, ts
    ))
    conn.commit()
    return {"status": "ok", "notice_id": notice_id}


def _update_notice_status(conn, args):
    ts = now_iso()
    conn.execute("""
        UPDATE notices SET status=?, resolution_note=?, ai_draft_path=?, updated_at=?
        WHERE notice_id=?
    """, (
        args["status"], args.get("resolution_note"), args.get("ai_draft_path"),
        ts, args["notice_id"]
    ))
    conn.commit()
    return {"status": "ok"}


def _list_notices(conn, args):
    q = "SELECT n.*, c.name as client_name FROM notices n LEFT JOIN clients c ON n.client_id=c.client_id WHERE 1=1"
    params = []
    if args.get("client_id"):
        q += " AND n.client_id=?"
        params.append(args["client_id"])
    if args.get("status"):
        q += " AND n.status=?"
        params.append(args["status"])
    if args.get("portal"):
        q += " AND n.portal=?"
        params.append(args["portal"])
    q += " ORDER BY n.due_date ASC"
    limit = min(int(args.get("limit", 50)), 200)
    q += f" LIMIT {limit}"
    rows = conn.execute(q, params).fetchall()
    return {"status": "ok", "count": len(rows), "notices": [row_to_dict(r) for r in rows]}


def _log_compliance_event(conn, args):
    import uuid
    ts = now_iso()
    task_id = args.get("task_id") or f"t_{uuid.uuid4().hex[:10]}"
    conn.execute("""
        INSERT INTO compliance_calendar (task_id, client_id, form_type, period,
            due_date, description, status, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(task_id) DO UPDATE SET
            status=excluded.status, due_date=excluded.due_date,
            description=excluded.description, updated_at=excluded.updated_at
    """, (
        task_id, args.get("client_id"), args["form_type"], args.get("period"),
        args["due_date"], args.get("description", ""), args.get("status", "pending"),
        ts, ts
    ))
    conn.commit()
    return {"status": "ok", "task_id": task_id}


def _mark_filing_complete(conn, args):
    ts = now_iso()
    filed_date = args.get("filed_date") or datetime.date.today().isoformat()
    conn.execute("""
        UPDATE compliance_calendar
        SET status='filed', filed_date=?, filed_by=?, notes=?, updated_at=?
        WHERE task_id=?
    """, (
        filed_date, args.get("filed_by", "CA"), args.get("notes"), ts, args["task_id"]
    ))
    conn.commit()
    return {"status": "ok"}


def _get_due_dates(conn, args):
    today = datetime.date.today().isoformat()
    days_ahead = int(args.get("days_ahead", 30))
    end_date = (datetime.date.today() + datetime.timedelta(days=days_ahead)).isoformat()
    q = """
        SELECT cc.*, c.name as client_name
        FROM compliance_calendar cc
        LEFT JOIN clients c ON cc.client_id=c.client_id
        WHERE cc.due_date BETWEEN ? AND ?
    """
    params: list = [today, end_date]
    if not args.get("include_filed"):
        q += " AND cc.status NOT IN ('filed','completed','nil')"
    if args.get("client_id"):
        q += " AND cc.client_id=?"
        params.append(args["client_id"])
    q += " ORDER BY cc.due_date ASC LIMIT 100"
    rows = conn.execute(q, params).fetchall()
    return {"status": "ok", "count": len(rows), "due_dates": [row_to_dict(r) for r in rows]}


def _query_audit_trail(conn, args):
    q = "SELECT * FROM audit_trail WHERE 1=1"
    params = []
    if args.get("client_id"):
        q += " AND client_id=?"
        params.append(args["client_id"])
    if args.get("from_date"):
        q += " AND ts >= ?"
        params.append(args["from_date"])
    if args.get("to_date"):
        q += " AND ts <= ?"
        params.append(args["to_date"])
    if args.get("tool_prefix"):
        q += " AND tool LIKE ?"
        params.append(f"{args['tool_prefix']}%")
    if args.get("severity"):
        q += " AND severity=?"
        params.append(args["severity"])
    q += " ORDER BY ts DESC"
    limit = min(int(args.get("limit", 100)), 1000)
    q += f" LIMIT {limit}"
    rows = conn.execute(q, params).fetchall()
    return {"status": "ok", "count": len(rows), "entries": [row_to_dict(r) for r in rows]}


def _log_audit_entry(conn, args):
    ts = now_iso()
    conn.execute("""
        INSERT INTO audit_trail (ts, session_id, user_id, tool, severity, client_id,
            amount, input_summary, success, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        ts,
        args.get("session_id", os.environ.get("CLAUDE_SESSION_ID", "")),
        os.environ.get("CLAUDE_USER_ID", ""),
        args["tool"],
        args.get("severity", "info"),
        args.get("client_id"),
        args.get("amount"),
        args.get("input_summary", ""),
        1 if args.get("success", True) else 0,
        args.get("notes", "")
    ))
    conn.commit()
    return {"status": "ok"}


# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
