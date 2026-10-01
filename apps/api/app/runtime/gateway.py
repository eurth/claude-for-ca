import json
import re
from typing import Any

import httpx

from app.config import settings

JSON_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


class GatewayResult:
    def __init__(self, text: str, provider: str, model: str):
        self.text = text
        self.provider = provider
        self.model = model

    def parsed(self) -> dict[str, Any]:
        match = JSON_FENCE.search(self.text)
        blob = match.group(1) if match else None
        if blob is None:
            start = self.text.find("{")
            end = self.text.rfind("}")
            if start >= 0 and end > start:
                blob = self.text[start : end + 1]
        if not blob:
            return {"summary": self.text[:4000], "artifacts": []}
        try:
            return json.loads(blob)
        except json.JSONDecodeError:
            return {"summary": self.text[:4000], "artifacts": []}


def _models(effort: str) -> tuple[str, str]:
    provider = (settings.llm_provider or "mock").lower()
    if provider == "openrouter" and settings.openrouter_api_key:
        high = settings.llm_model_high or "nvidia/nemotron-3-super-120b-a12b:free"
        low = settings.llm_model_low or "nvidia/nemotron-3-super-120b-a12b:free"
        return provider, (low if effort == "low" else high)
    if provider == "anthropic" and settings.anthropic_api_key:
        high = settings.llm_model_high or "claude-sonnet-4-5"
        low = settings.llm_model_low or "claude-haiku-4-5"
        return provider, (low if effort == "low" else high)
    if provider == "openai" and settings.openai_api_key:
        high = settings.llm_model_high or "gpt-4o"
        low = settings.llm_model_low or "gpt-4o-mini"
        return provider, (low if effort == "low" else high)
    if provider == "gemini" and settings.gemini_api_key:
        high = settings.llm_model_high or "gemini-2.0-flash"
        low = settings.llm_model_low or "gemini-2.0-flash"
        return provider, (low if effort == "low" else high)
    return "mock", "mock"


def complete(
    messages: list[dict], effort: str = "medium", feature_id: str | None = None
) -> GatewayResult:
    provider, model = _models(effort)
    if provider == "anthropic":
        text = _anthropic(messages, model)
    elif provider == "openai":
        text = _openai(messages, model)
    elif provider == "gemini":
        text = _gemini(messages, model)
    elif provider == "openrouter":
        text, model = _openrouter(messages, model)
    else:
        text = _mock(messages, feature_id)
    return GatewayResult(text, provider, model)


def _system_and_user(messages: list[dict]) -> tuple[str, str]:
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    user = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
    return system, user


def _anthropic(messages: list[dict], model: str) -> str:
    system, user = _system_and_user(messages)
    body = {
        "model": model,
        "max_tokens": 4096,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    with httpx.Client(timeout=90) as client:
        r = client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
        )
        r.raise_for_status()
        data = r.json()
    return "".join(part.get("text", "") for part in data.get("content", []) if part.get("type") == "text")


def _openai(messages: list[dict], model: str) -> str:
    with httpx.Client(timeout=90) as client:
        r = client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={"model": model, "messages": messages, "temperature": 0.1},
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def _gemini(messages: list[dict], model: str) -> str:
    system, user = _system_and_user(messages)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    with httpx.Client(timeout=90) as client:
        r = client.post(
            url,
            params={"key": settings.gemini_api_key},
            json={
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
            },
        )
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]


OPENROUTER_FREE_FALLBACKS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "openrouter/free",
]


def _openrouter_retryable(exc: Exception) -> bool:
    msg = str(exc).lower()
    tokens = ("404", "502", "503", "504", "429", "no endpoints", "not found", "unavailable", "aborted", "empty reply")
    return any(t in msg for t in tokens)


def _openrouter(messages: list[dict], model: str) -> tuple[str, str]:
    tried = []
    last_error = None
    candidates = [model] + [m for m in OPENROUTER_FREE_FALLBACKS if m != model]
    for candidate in candidates:
        tried.append(candidate)
        try:
            return _openrouter_once(messages, candidate), candidate
        except RuntimeError as exc:
            last_error = exc
            if _openrouter_retryable(exc):
                continue
            raise
    raise RuntimeError(f"OpenRouter free models unavailable ({', '.join(tried)}): {last_error}")


def _openrouter_once(messages: list[dict], model: str) -> str:
    with httpx.Client(timeout=120) as client:
        r = client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "HTTP-Referer": settings.openrouter_site_url,
                "X-Title": settings.openrouter_app_name,
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 4096,
            },
        )
        if r.status_code >= 400:
            detail = r.text[:400].replace(settings.openrouter_api_key, "")
            raise RuntimeError(f"OpenRouter {r.status_code}: {detail}")
        data = r.json()
    message = (data.get("choices") or [{}])[0].get("message") or {}
    content = message.get("content") or message.get("reasoning") or ""
    if not str(content).strip():
        raise RuntimeError("OpenRouter empty reply")
    return content


def _mock(messages: list[dict], feature_id: str | None = None) -> str:
    blob = " ".join(m["content"] for m in messages).lower()
    fid = (feature_id or "").lower()
    if fid == "discover":
        suggestion = "pdf-data-extractor"
        if "3b" in blob or "gstr" in blob:
            suggestion = "gstr3b-review"
        elif "bank" in blob:
            suggestion = "bank-statement-processor"
        elif "tally" in blob:
            suggestion = "tally-import-builder"
        elif "notice" in blob:
            suggestion = "notice-triage"
        elif "master" in blob or "excel" in blob or "workbook" in blob:
            suggestion = "master-accounts-sheet"
        payload = {
            "summary": f"Use the feature: {suggestion}",
            "suggested_feature_id": suggestion,
            "artifacts": [{"type": "router_suggestion", "title": "Suggested feature", "data": {"id": suggestion}}],
        }
        return "```json\n" + json.dumps(payload, indent=2) + "\n```"

    from app.runtime.catalog import get_feature

    try:
        feature = get_feature(fid)
    except KeyError:
        feature = {
            "name": fid or "Job",
            "produces": ["note"],
            "filing_class": None,
        }
    artifacts = []
    for kind in feature.get("produces") or ["note"]:
        artifacts.append(
            {
                "type": kind,
                "title": kind.replace("_", " ").title() + " (draft)",
                "data": {"notes": ["Upload source documents, then run again for a full working."]},
            }
        )
    payload = {
        "summary": f"Draft {feature.get('name')}. Upload source documents and run again. Nothing is filed from this app.",
        "artifacts": artifacts,
    }
    if feature.get("filing_class"):
        payload["approval"] = {"kind": feature["filing_class"]}
    return "```json\n" + json.dumps(payload, indent=2) + "\n```"
