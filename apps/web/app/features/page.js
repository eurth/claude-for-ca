"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Shell from "../../components/Shell";
import { api } from "../../lib/api";

export default function FeaturesPage() {
  return (
    <Suspense fallback={<p className="muted">Loading…</p>}>
      <FeaturesInner />
    </Suspense>
  );
}

function FeaturesInner() {
  const params = useSearchParams();
  const router = useRouter();
  const [features, setFeatures] = useState([]);
  const [clients, setClients] = useState(null);
  const [featureId, setFeatureId] = useState("pdf-data-extractor");
  const [entityId, setEntityId] = useState(params.get("entity") || "");
  const [regId, setRegId] = useState("");
  const [period, setPeriod] = useState("2026-04");
  const [note, setNote] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api("/api/features").then((d) => setFeatures(d.features || []));
    api("/api/clients").then((d) => {
      setClients(d);
      if (!entityId && d.entities?.[0]) setEntityId(d.entities[0].id);
    });
  }, []);

  const entity = useMemo(
    () => (clients?.entities || []).find((e) => e.id === entityId),
    [clients, entityId]
  );
  const grouped = useMemo(() => {
    const order = [];
    const map = {};
    for (const f of features) {
      if (!map[f.section]) {
        map[f.section] = [];
        order.push(f.section);
      }
      map[f.section].push(f);
    }
    return order.map((section) => ({ section, items: map[section] }));
  }, [features]);

  useEffect(() => {
    const regs = entity?.registrations || [];
    if (!regs.length) {
      setRegId("");
      return;
    }
    if (!regId || !regs.some((r) => r.id === regId)) {
      const gstin = regs.find((r) => r.kind === "gstin");
      setRegId((gstin || regs[0]).id);
    }
  }, [entityId, entity]);

  async function start(e, nextId) {
    if (e) e.preventDefault();
    const fid = nextId || featureId;
    if (nextId) setFeatureId(nextId);
    const job = features.find((f) => f.id === fid) || features.find((f) => f.id === featureId);
    setErr("");
    if (!entityId) {
      setErr("Select a client first.");
      return;
    }
    if (job?.scope === "gstin" && !regId) {
      setErr("Select a GSTIN for this job.");
      return;
    }
    setBusy(true);
    try {
      const created = await api("/api/workpacks", {
        method: "POST",
        body: JSON.stringify({
          feature_id: fid,
          entity_id: entityId,
          registration_id: regId || null,
          period: period || null,
          note: note || null,
        }),
      });
      router.push(`/workpacks/${created.id}`);
    } catch (ex) {
      setErr(ex.message);
      setBusy(false);
    }
  }

  return (
    <Shell>
      <h1>Work</h1>
      <p className="muted">
        Choose client, GSTIN and period, then click a job. Upload source files on the next screen, then Run.
      </p>
      <form onSubmit={(e) => start(e)} style={{ maxWidth: 520, marginBottom: 20 }}>
        <label>Client</label>
        <select value={entityId} onChange={(e) => setEntityId(e.target.value)} required>
          <option value="">Select client…</option>
          {(clients?.entities || []).map((e) => (
            <option key={e.id} value={e.id}>
              {e.name}
            </option>
          ))}
        </select>
        <label>GSTIN / registration (required for GST jobs)</label>
        <select value={regId} onChange={(e) => setRegId(e.target.value)}>
          <option value="">—</option>
          {(entity?.registrations || []).map((r) => (
            <option key={r.id} value={r.id}>
              {r.kind} {r.value}
              {r.label ? ` (${r.label})` : ""}
            </option>
          ))}
        </select>
        <label>Period (month YYYY-MM or FY)</label>
        <input value={period} onChange={(e) => setPeriod(e.target.value)} />
        <label>Note (optional)</label>
        <textarea
          rows={2}
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="e.g. April purchase invoices from client WhatsApp"
        />
        {err ? <p className="err">{err}</p> : null}
      </form>
      {grouped.map((g) => (
        <div key={g.section} style={{ marginTop: 28 }}>
          <h2>{g.section}</h2>
          <div className="grid">
            {g.items.map((f) => (
              <button
                type="button"
                key={f.id}
                className={`card ${featureId === f.id ? "selected" : ""}`}
                disabled={busy}
                onClick={() => start(null, f.id)}
              >
                <h3>{f.name}</h3>
                <p className="muted">{f.description}</p>
                <p style={{ marginTop: 8 }}>
                  <span className="btn">{busy && featureId === f.id ? "Opening…" : "Start job"}</span>
                </p>
              </button>
            ))}
          </div>
        </div>
      ))}
    </Shell>
  );
}
