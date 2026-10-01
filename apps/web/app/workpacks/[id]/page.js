"use client";

import { Suspense, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Shell from "../../../components/Shell";
import ArtifactView from "../../../components/ArtifactView";
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
  const [pack, setPack] = useState(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

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

  async function upload(ev) {
    const files = [...(ev.target.files || [])];
    if (!files.length) return;
    setBusy(true);
    setErr("");
    try {
      const token = getToken();
      for (const file of files) {
        const fd = new FormData();
        fd.append("upload", file);
        const lower = file.name.toLowerCase();
        let kind = "upload";
        if (lower.includes("2b")) kind = "gstr2b_excel";
        else if (lower.includes("hdfc") || lower.includes("statement") || lower.includes("bank")) kind = "bank_pdf";
        else if (lower.includes("inv") || lower.includes("invoice")) kind = "purchase_invoice";
        fd.append("artifact_type", kind);
        const res = await fetch(`${apiUrl()}/api/workpacks/${id}/files`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
          body: fd,
        });
        if (!res.ok) throw new Error("Upload failed");
      }
      await load();
    } catch (ex) {
      setErr(ex.message);
    } finally {
      setBusy(false);
      ev.target.value = "";
    }
  }

  async function downloadExcel(artifact) {
    const token = getToken();
    const res = await fetch(`${apiUrl()}/api/workpacks/${pack.id}/xlsx/${artifact.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = (artifact.title || "working").replaceAll(" ", "_") + ".xlsx";
    link.click();
  }

  async function download(artifact) {
    const token = getToken();
    const res = await fetch(`${apiUrl()}/api/workpacks/${pack.id}/files/${artifact.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = artifact.type === "tally_xml" ? "tally_import.xml" : artifact.title;
    link.click();
  }

  if (!pack) {
    return (
      <Shell>
        <p className="muted">{err || "Loading workpack…"}</p>
      </Shell>
    );
  }

  const pending = (pack.approvals || []).find((a) => a.status === "pending");
  const uploaded = (pack.artifacts || []).filter((a) => a.is_input);
  const outputs = (pack.artifacts || []).filter((a) => !a.is_input);

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
        Upload the source PDFs first, then Run. A later job for the same client and period can reuse this working.
        Nothing is filed from this screen.
      </p>
      <div className="row" style={{ margin: "1rem 0" }}>
        <input type="file" multiple onChange={upload} disabled={busy} />
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
        <p className="muted">Upload files, then click Run job.</p>
      )}
      {pending ? (
        <div className="card" style={{ margin: "1rem 0" }}>
          <h3>Waiting for Partner approval</h3>
          <p className="muted">{pending.kind.replaceAll("_", " ")}</p>
          <pre>{pending.checklist}</pre>
          <Link href="/approvals">Open approval inbox</Link>
        </div>
      ) : null}
      <h2>Uploaded files</h2>
      {uploaded.length ? (
        uploaded.map((a) => (
          <ArtifactView key={a.id} artifact={a} pack={pack} onDownload={download} onExcel={downloadExcel} />
        ))
      ) : (
        <p className="muted">No files yet.</p>
      )}
      <h2>Working</h2>
      {outputs.length ? (
        outputs.map((a) => (
          <ArtifactView key={a.id} artifact={a} pack={pack} onDownload={download} onExcel={downloadExcel} />
        ))
      ) : (
        <p className="muted">No working yet.</p>
      )}
    </Shell>
  );
}
