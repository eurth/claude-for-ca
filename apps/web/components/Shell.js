"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { clearSession, getUser } from "../lib/api";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/clients", label: "Clients" },
  { href: "/features", label: "Work" },
  { href: "/approvals", label: "Approvals" },
  { href: "/audit", label: "Audit log" },
];

export default function Shell({ children }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const u = getUser();
    if (!u) {
      router.replace("/login");
      return;
    }
    setUser(u);
  }, [router]);

  if (!user) return <div className="main muted">Loading…</div>;

  const links = LINKS.filter((l) => {
    if (l.href === "/approvals") return user.role === "partner" || user.role === "manager";
    return true;
  });
  if (user.role === "partner") links.push({ href: "/settings", label: "Settings" });

  return (
    <div className="shell">
      <aside className="nav">
        <div className="firm">{user.firm_name}</div>
        <div className="role">
          {user.name} · {user.role}
        </div>
        {links.map((l) => (
          <Link key={l.href} href={l.href} className={pathname === l.href ? "active" : ""}>
            {l.label}
          </Link>
        ))}
        <button
          className="out"
          onClick={() => {
            clearSession();
            router.replace("/login");
          }}
        >
          Sign out
        </button>
      </aside>
      <div className="main">{children}</div>
    </div>
  );
}
