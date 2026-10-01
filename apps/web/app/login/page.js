"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, setSession } from "../../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("partner@gorantla.local");
  const [password, setPassword] = useState("changeme");
  const [err, setErr] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setErr("");
    try {
      const data = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setSession(data.token, data.user);
      router.replace("/");
    } catch (ex) {
      setErr(ex.message);
    }
  }

  return (
    <div className="login">
      <h1>Practice</h1>
      <p className="muted">Sign in with your firm account. Work is always tied to a client.</p>
      <form onSubmit={onSubmit}>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="username" />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
        {err ? <p className="err">{err}</p> : null}
        <p>
          <button className="btn" type="submit">
            Sign in
          </button>
        </p>
      </form>
    </div>
  );
}
