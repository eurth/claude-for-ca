"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "../../components/Shell";
import { api, getUser } from "../../lib/api";

export default function ApprovalsPage() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");
  const role = getUser()?.role;

  function load() {
    api("/api/approvals")
      .then((d) => setRows(d.approvals || []))
      .catch((e) => setErr(e.message));
  }

  useEffect(load, []);

  async function decide(id, decision) {
    setErr("");
    try {
      await api(`/api/approvals/${id}`, { method: "POST", body: JSON.stringify({ decision }) });
      load();
    } catch (e) {
      setErr(e.message);
    }
  }

  return (
    <Shell>
      <h1>Approvals</h1>
      <p className="muted">Filing-class packs (GSTR-3B, Tally XML, notice replies) wait here. Nothing is sent to a government portal from this screen.</p>
      {err ? <p className="err">{err}</p> : null}
      {rows.map((a) => (
        <div className="card" key={a.id} style={{ marginBottom: 12 }}>
          <h3>
            <Link href={`/workpacks/${a.workpack_id}`}>{a.title}</Link>
          </h3>
          <p className="muted">{a.kind}</p>
          <pre>{a.checklist}</pre>
          {role === "partner" ? (
            <div className="row">
              <button className="btn" onClick={() => decide(a.id, "approve")}>
                Approve
              </button>
              <button className="btn secondary" onClick={() => decide(a.id, "deny")}>
                Deny
              </button>
            </div>
          ) : (
            <p className="muted">Partner sign-off required.</p>
          )}
        </div>
      ))}
      {!rows.length ? <p className="muted">No packs waiting.</p> : null}
    </Shell>
  );
}
