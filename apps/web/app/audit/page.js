"use client";

import { useEffect, useState } from "react";
import Shell from "../../components/Shell";
import { api } from "../../lib/api";

export default function AuditPage() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    api("/api/audit")
      .then((d) => setRows(d.events || []))
      .catch((e) => setErr(e.message));
  }, []);

  return (
    <Shell>
      <h1>Audit log</h1>
      <p className="muted">Who ran which job. Interns do not see model names here; Partners see them on the workpack after a run.</p>
      {err ? <p className="err">{err}</p> : null}
      <table>
        <thead>
          <tr>
            <th>When</th>
            <th>Action</th>
            <th>Detail</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((e) => (
            <tr key={e.id}>
              <td>{e.at}</td>
              <td>{e.action}</td>
              <td>{e.detail}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Shell>
  );
}
