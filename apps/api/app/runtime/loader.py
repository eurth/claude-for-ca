from pathlib import Path


def load_skill(feature_id: str) -> str:
    from app.config import settings

    candidates = [
        Path(settings.packs_dir) / feature_id / "SKILL.md",
        Path.cwd() / "packs" / feature_id / "SKILL.md",
        Path(__file__).resolve().parents[4] / "packs" / feature_id / "SKILL.md",
    ]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(f"Skill pack missing: {feature_id}")
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", "")
    return text.strip()
