"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Shell from "../../../components/Shell";
import { api } from "../../../lib/api";

export default function EntityPage() {
  const { id } = useParams();
  const [e, setE] = useState(null);
  const [packs, setPacks] = useState([]);

  useEffect(() => {
    if (!id) return;
    api(`/api/clients/${id}`).then(setE).catch(() => {});
    api(`/api/workpacks?entity_id=${id}`)
      .then((d) => setPacks(d.workpacks || []))
      .catch(() => {});
  }, [id]);

  if (!e) {
    return (
      <Shell>
        <p className="muted">Loading client…</p>
      </Shell>
    );
  }

  return (
    <Shell>
      <p className="muted">
        <Link href="/clients">Clients</Link>
      </p>
      <h1>{e.name}</h1>
      <p className="muted">
        PAN {e.pan || "—"} · {e.entity_type || "entity"}
      </p>
      <h2>Registrations</h2>
      <ul>
        {e.registrations.map((r) => (
          <li key={r.id}>
            <strong>{r.kind}</strong> {r.value} {r.label ? `(${r.label})` : ""} {r.state || ""}
          </li>
        ))}
      </ul>
      <AddRegistration entityId={e.id} onSaved={() => api(`/api/clients/${id}`).then(setE)} />
      <h2>Notices</h2>
      <ul>
        {(e.notices || []).map((n) => (
          <li key={n.id}>
            {n.portal}: {n.summary || "Notice"} <span className={`pill ${n.status}`}>{n.status}</span>
          </li>
        ))}
        {!(e.notices || []).length ? <li className="muted">None on file</li> : null}
      </ul>
      <h2>Open dues</h2>
      <ul>
        {(e.dues || []).map((d, i) => (
          <li key={i}>
            {d.form_type} {d.period} — due {d.due_date}
          </li>
        ))}
        {!(e.dues || []).length ? <li className="muted">None listed</li> : null}
      </ul>
      <p>
        <Link className="btn" href={`/features?entity=${e.id}`}>
          Start work
        </Link>
      </p>
      <h2>Workpacks</h2>
      <ul>
        {packs.map((p) => (
          <li key={p.id}>
            <Link href={`/workpacks/${p.id}`}>{p.title}</Link> <span className={`pill ${p.status}`}>{p.status}</span>
          </li>
        ))}
      </ul>
    </Shell>
  );
}

function AddRegistration({ entityId, onSaved }) {
  const [value, setValue] = useState("");
  const [state, setState] = useState("");
  const [err, setErr] = useState("");

  async function save(ev) {
    ev.preventDefault();
    setErr("");
    try {
      await api(`/api/clients/${entityId}/registrations`, {
        method: "POST",
        body: JSON.stringify({ kind: "gstin", value, state, label: state || "GSTIN" }),
      });
      setValue("");
      setState("");
      onSaved();
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <form onSubmit={save} style={{ maxWidth: 420, marginBottom: 24 }}>
      <h3>Add GSTIN</h3>
      <label>GSTIN</label>
      <input value={value} onChange={(e) => setValue(e.target.value)} required />
      <label>State</label>
      <input value={state} onChange={(e) => setState(e.target.value)} />
      {err ? <p className="err">{err}</p> : null}
      <p>
        <button className="btn secondary" type="submit">
          Add registration
        </button>
      </p>
    </form>
  );
}
