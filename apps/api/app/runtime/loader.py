import re
from pathlib import Path

INTERPOLATOR = re.compile(r"!`[^`]+`")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_skill(feature_id: str) -> str:
    from app.config import settings
    from app.runtime.catalog import get_feature

    feature = get_feature(feature_id)
    rel = feature.get("source") or f"packs/{feature_id}/SKILL.md"
    candidates = [
        Path(settings.packs_dir) / feature_id / "SKILL.md",
        Path.cwd() / "packs" / feature_id / "SKILL.md",
        _repo_root() / "packs" / feature_id / "SKILL.md",
        _repo_root() / rel,
        Path.cwd() / rel,
    ]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(f"Skill pack missing: {feature_id}")
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", "").replace("${CLAUDE_PLUGIN_DATA}", "")
    text = INTERPOLATOR.sub("", text)
    return text.strip()
