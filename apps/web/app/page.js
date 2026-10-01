"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Shell from "../components/Shell";
import { api } from "../lib/api";

export default function HomePage() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    api("/api/home")
      .then(setData)
      .catch((e) => setErr(e.message));
  }, []);

  return (
    <Shell>
      <h1>This week</h1>
      <p className="muted">Due dates, recent work, and packs waiting for Partner review.</p>
      {err ? <p className="err">{err}</p> : null}
      {data ? (
        <>
          <div className="grid" style={{ marginTop: 16 }}>
            <div className="card">
              <div className="muted">Waiting for approval</div>
              <h2>{data.pending_approvals}</h2>
              <Link href="/approvals">Open inbox</Link>
            </div>
          </div>
          <h2 style={{ marginTop: 28 }}>Compliance dues</h2>
          <table>
            <thead>
              <tr>
                <th>Client</th>
                <th>Form</th>
                <th>Period</th>
                <th>Due</th>
              </tr>
            </thead>
            <tbody>
              {data.dues.map((d, i) => (
                <tr key={i}>
                  <td>{d.entity}</td>
                  <td>{d.form_type}</td>
                  <td>{d.period}</td>
                  <td>{d.due_date}</td>
                </tr>
              ))}
              {!data.dues.length ? (
                <tr>
                  <td colSpan={4} className="muted">
                    No open dues in the calendar yet.
                  </td>
                </tr>
              ) : null}
            </tbody>
          </table>
          <h2 style={{ marginTop: 28 }}>Recent work</h2>
          <ul>
            {data.recent.map((p) => (
              <li key={p.id}>
                <Link href={`/workpacks/${p.id}`}>{p.title}</Link>{" "}
                <span className={`pill ${p.status}`}>{p.status}</span> · {p.entity}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="muted">Loading…</p>
      )}
    </Shell>
  );
}
