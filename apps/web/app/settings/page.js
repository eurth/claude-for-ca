"use client";

import { useEffect, useState } from "react";
import Shell from "../../components/Shell";
import { api, getUser } from "../../lib/api";

export default function SettingsPage() {
  const role = getUser()?.role;
  const [data, setData] = useState(null);
  const [hitl, setHitl] = useState("100000");
  const [letterhead, setLetterhead] = useState("");
  const [err, setErr] = useState("");
  const [saved, setSaved] = useState("");

  useEffect(() => {
    api("/api/settings")
      .then((d) => {
        setData(d);
        setHitl(String(d.hitl_threshold ?? 100000));
        setLetterhead(d.letterhead || "");
      })
      .catch((e) => setErr(e.message));
  }, []);

  async function save(e) {
    e.preventDefault();
    setErr("");
    setSaved("");
    try {
      await api("/api/settings", {
        method: "PATCH",
        body: JSON.stringify({ hitl_threshold: Number(hitl), letterhead }),
      });
      setSaved("Saved.");
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <Shell>
      <h1>Firm settings</h1>
      <p className="muted">Partner-only. API keys stay in the host environment — they are never shown here.</p>
      {err ? <p className="err">{err}</p> : null}
      {saved ? <p>{saved}</p> : null}
      {data ? (
        <form onSubmit={save} style={{ maxWidth: 560 }}>
          <p>
            <strong>{data.firm_name}</strong>
            <span className="muted"> · {data.ca_name}</span>
          </p>
          <label>HITL amount threshold (Rs.)</label>
          <input value={hitl} onChange={(e) => setHitl(e.target.value)} disabled={role !== "partner"} />
          <label>Letterhead / sign-off text</label>
          <textarea rows={5} value={letterhead} onChange={(e) => setLetterhead(e.target.value)} disabled={role !== "partner"} />
          {data.providers_configured ? (
            <>
              <h2 style={{ marginTop: 24 }}>Model gateway (host)</h2>
              <p className="muted">Active provider: {data.llm_provider}. Keys are configured in Coolify, not in this form.</p>
              <ul>
                <li>OpenRouter: {data.providers_configured.openrouter ? "configured" : "not set"}</li>
                <li>Anthropic: {data.providers_configured.anthropic ? "configured" : "not set"}</li>
                <li>OpenAI: {data.providers_configured.openai ? "configured" : "not set"}</li>
                <li>Gemini: {data.providers_configured.gemini ? "configured" : "not set"}</li>
              </ul>
            </>
          ) : null}
          {role === "partner" ? (
            <p>
              <button className="btn" type="submit">
                Save
              </button>
            </p>
          ) : (
            <p className="muted">Only a Partner can change these settings.</p>
          )}
        </form>
      ) : (
        <p className="muted">Loading…</p>
      )}
    </Shell>
  );
}
