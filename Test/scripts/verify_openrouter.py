"""Ping OpenRouter free models. Reads OPENROUTER_API_KEY from repo-root .env. Never prints the key."""

from __future__ import annotations

import json
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
TEST = Path(__file__).resolve().parents[1]
OUT = TEST / "results"
OUT.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    "openrouter/free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "qwen/qwen3.8-27b:free",
    "liquid/lfm-2.5-2.6b:free",
    "inclusionai/ling-3.0-flash-sante:free",
    "poolside/laguna-s-2.1:free",
    "dots-studio/dots-3-note-preview:free",
]


def _key() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("OPENROUTER_API_KEY missing in .env")


def _headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "http://127.0.0.1:3000",
        "X-Title": "for-ca",
    }


def ping(model: str, key: str) -> dict:
    t0 = time.time()
    try:
        r = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=_headers(key),
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Reply with exactly OK"}],
                "max_tokens": 64,
                "temperature": 0,
            },
            timeout=50,
        )
        elapsed = round(time.time() - t0, 2)
        data = r.json()
        if r.status_code >= 400:
            err = str((data.get("error") or data))[:240]
            return {"id": model, "ok": False, "status": r.status_code, "seconds": elapsed, "error": err}
        msg = ((data.get("choices") or [{}])[0].get("message") or {})
        text = (msg.get("content") or msg.get("reasoning") or "").strip()
        return {
            "id": model,
            "ok": bool(text),
            "status": r.status_code,
            "seconds": elapsed,
            "routed": data.get("model") or model,
            "reply": text[:120],
        }
    except Exception as exc:
        return {"id": model, "ok": False, "status": 0, "seconds": round(time.time() - t0, 2), "error": str(exc)[:240]}


def main() -> None:
    key = _key()
    catalog = httpx.get("https://openrouter.ai/api/v1/models", headers=_headers(key), timeout=30)
    catalog.raise_for_status()
    free_ids = []
    for item in catalog.json().get("data") or []:
        mid = item.get("id") or ""
        if ":free" in mid:
            free_ids.append(mid)
    rows = [ping(mid, key) for mid in CANDIDATES]
    payload = {
        "free_catalog": sorted(free_ids),
        "probes": rows,
        "working": [r["id"] for r in rows if r.get("ok")],
        "gemma_ok": [r["id"] for r in rows if r.get("ok") and "gemma" in r["id"]],
    }
    out = OUT / "openrouter_probe.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("working:", payload["working"])
    print("gemma_ok:", payload["gemma_ok"])
    print("wrote", out)


if __name__ == "__main__":
    main()
