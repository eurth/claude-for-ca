"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "../../components/Shell";
import { api, getUser } from "../../lib/api";

export default function ClientsPage() {
  const [data, setData] = useState(null);
  const [form, setForm] = useState({
    name: "",
    pan: "",
    gstin: "",
    group_name: "",
    entity_type: "Private Ltd",
  });
  const [err, setErr] = useState("");
  const canEdit = ["partner", "manager"].includes(getUser()?.role);

  function load() {
    api("/api/clients")
      .then(setData)
      .catch((e) => setErr(e.message));
  }

  useEffect(load, []);

  async function create(e) {
    e.preventDefault();
    setErr("");
    try {
      await api("/api/clients", { method: "POST", body: JSON.stringify(form) });
      setForm({ name: "", pan: "", gstin: "", group_name: "", entity_type: "Private Ltd" });
      load();
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <Shell>
      <h1>Clients</h1>
      <p className="muted">Group → legal entity (PAN) → GSTIN / TAN. Open an entity to run work.</p>
      {err ? <p className="err">{err}</p> : null}
      <div className="grid" style={{ marginTop: 16 }}>
        {(data?.entities || []).map((e) => (
          <Link key={e.id} href={`/clients/${e.id}`} className="card">
            <h3>{e.name}</h3>
            <p className="muted">PAN {e.pan || "—"}</p>
            {(e.registrations || []).map((r) => (
              <div key={r.id} className="pill">
                {r.kind}: {r.value}
              </div>
            ))}
          </Link>
        ))}
      </div>
      {canEdit ? (
        <>
          <h2 style={{ marginTop: 32 }}>Add entity</h2>
          <form onSubmit={create} style={{ maxWidth: 480 }}>
            <label>Legal name</label>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            <label>Group (optional)</label>
            <input value={form.group_name} onChange={(e) => setForm({ ...form, group_name: e.target.value })} />
            <label>PAN</label>
            <input value={form.pan} onChange={(e) => setForm({ ...form, pan: e.target.value })} />
            <label>GSTIN (optional extra GSTINs can be added later)</label>
            <input value={form.gstin} onChange={(e) => setForm({ ...form, gstin: e.target.value })} />
            <p>
              <button className="btn" type="submit">
                Save client
              </button>
            </p>
          </form>
        </>
      ) : null}
    </Shell>
  );
}
