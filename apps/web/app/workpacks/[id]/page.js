"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import Link from "next/link";
import Shell from "../../../components/Shell";
import { api, apiUrl, getToken } from "../../../lib/api";

export default function WorkpackPage() {
  return (
    <Suspense fallback={<p className="muted">Loading workpack…</p>}>
      <WorkpackInner />
    </Suspense>
  );
}

function WorkpackInner() {
  const { id } = useParams();
  const search = useSearchParams();
  const [pack, setPack] = useState(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const autoRan = useRef(false);

  function load() {
    return api(`/api/workpacks/${id}`).then(setPack).catch((e) => setErr(e.message));
  }

  useEffect(() => {
    if (id) load();
  }, [id]);

  async function run() {
    setBusy(true);
    setErr("");
    try {
      const data = await api(`/api/workpacks/${id}/run`, { method: "POST" });
      setPack(data);
    } catch (ex) {
      setErr(ex.message);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (!pack || !id || autoRan.current) return;
    const key = `forca_autorun_${id}`;
    if (search.get("autorun") === "1" && pack.status === "draft") {
      if (typeof window !== "undefined" && sessionStorage.getItem(key)) return;
      autoRan.current = true;
      if (typeof window !== "undefined") sessionStorage.setItem(key, "1");
      run();
    }
  }, [pack, search, id]);

  async function upload(ev) {
    const file = ev.target.files?.[0];
    if (!file) return;
    const fd = new FormData();
    fd.append("upload", file);
    fd.append("artifact_type", file.name.toLowerCase().includes("2b") ? "gstr2b_excel" : "upload");
    setBusy(true);
    setErr("");
    try {
      const token = getToken();
      const res = await fetch(`${apiUrl()}/api/workpacks/${id}/files`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: fd,
      });
      if (!res.ok) throw new Error("Upload failed");
      await load();
    } catch (ex) {
      setErr(ex.message);
    } finally {
      setBusy(false);
    }
  }

  if (!pack) {
    return (
      <Shell>
        <p className="muted">{err || "Loading workpack…"}</p>
      </Shell>
    );
  }

  const pending = (pack.approvals || []).find((a) => a.status === "pending");

  return (
    <Shell>
      <p className="muted">
        <Link href="/features">Work</Link>
      </p>
      <h1>{pack.title}</h1>
      <p>
        <span className={`pill ${pack.status}`}>{pack.status.replaceAll("_", " ")}</span>
        {pack.period ? ` · ${pack.period}` : ""}
      </p>
      <p className="muted">
        Upload source documents (invoices, 2B, bank PDF, notice), then run. Outputs stay on this client and period so
        the next job can reuse them. Nothing is filed from this screen.
      </p>
      <div className="row" style={{ margin: "1rem 0" }}>
        <input type="file" onChange={upload} disabled={busy} />
        <button className="btn" onClick={run} disabled={busy}>
          {busy ? "Working…" : pack.summary ? "Run again" : "Run job"}
        </button>
      </div>
      {err ? <p className="err">{err}</p> : null}
      {pack.summary ? (
        <>
          <h2>Summary</h2>
          <p>{pack.summary}</p>
        </>
      ) : (
        <p className="muted">Preparing a draft working…</p>
      )}
      {pending ? (
        <div className="card" style={{ margin: "1rem 0" }}>
          <h3>Waiting for Partner approval</h3>
          <p className="muted">{pending.kind.replaceAll("_", " ")}</p>
          <pre>{pending.checklist}</pre>
          <Link href="/approvals">Open approval inbox</Link>
        </div>
      ) : null}
      <h2>Documents & outputs</h2>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Title</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {(pack.artifacts || []).map((a) => (
            <tr key={a.id}>
              <td>
                {a.type} {a.is_input ? "(in)" : "(out)"}
              </td>
              <td>
                {a.title}
                {a.json ? <pre>{JSON.stringify(a.json, null, 2).slice(0, 1200)}</pre> : null}
              </td>
              <td>
                {a.has_file && (a.type !== "tally_xml" || pack.status === "approved") ? (
                  <button
                    className="btn secondary"
                    type="button"
                    onClick={async () => {
                      const token = getToken();
                      const res = await fetch(`${apiUrl()}/api/workpacks/${pack.id}/files/${a.id}`, {
                        headers: { Authorization: `Bearer ${token}` },
                      });
                      const blob = await res.blob();
                      const url = URL.createObjectURL(blob);
                      const link = document.createElement("a");
                      link.href = url;
                      link.download = a.type === "tally_xml" ? "tally_import.xml" : a.title;
                      link.click();
                    }}
                  >
                    {a.type === "tally_xml" ? "Download for Tally" : "Download"}
                  </button>
                ) : null}
                {a.type === "tally_xml" && pack.status !== "approved" ? (
                  <span className="muted">Waiting for Partner approval</span>
                ) : null}
              </td>
            </tr>
          ))}
          {!(pack.artifacts || []).length ? (
            <tr>
              <td colSpan={3} className="muted">
                No outputs yet.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </Shell>
  );
}
