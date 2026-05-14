#!/usr/bin/env python3
"""
validate.py — Validates all claude-for-ca plugin files.

Checks:
  1. All plugin.json files have required fields and correct dependencies.
  2. All SKILL.md files have valid YAML frontmatter with required fields.
  3. All agent.yaml files have required fields.

Usage:
  python scripts/validate.py
  python scripts/validate.py --plugin gst-compliance
  python scripts/validate.py --verbose
"""

import argparse
import os
import sys
from pathlib import Path

import yaml  # pip install pyyaml

ROOT = Path(__file__).parent.parent

REQUIRED_PLUGIN_FIELDS = {"id", "name", "version", "description", "author"}
REQUIRED_SKILL_FIELDS = {"name", "description", "when_to_use", "effort", "model"}
REQUIRED_AGENT_FIELDS = {"name", "description", "model", "effort"}
VALID_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
VALID_MODELS = {"claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"}

errors: list[str] = []
warnings: list[str] = []


def check_plugin_json(path: Path) -> None:
    import json
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"[PARSE ERROR] {path}: {e}")
        return

    for field in REQUIRED_PLUGIN_FIELDS:
        if field not in data:
            errors.append(f"[MISSING FIELD] {path}: missing '{field}'")

    plugin_id = data.get("id", "")
    if plugin_id != "claude-for-ca-core":
        deps = data.get("dependencies", [])
        if "claude-for-ca-core" not in deps:
            warnings.append(
                f"[DEPENDENCY WARNING] {path}: plugin '{plugin_id}' "
                f"does not declare dependency on claude-for-ca-core"
            )


def check_skill_md(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        errors.append(f"[NO FRONTMATTER] {path}: SKILL.md missing YAML frontmatter")
        return

    # Extract YAML block between first --- and second ---
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(f"[MALFORMED FRONTMATTER] {path}: cannot parse YAML frontmatter")
        return

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"[YAML ERROR] {path}: {e}")
        return

    if not isinstance(data, dict):
        errors.append(f"[EMPTY FRONTMATTER] {path}: frontmatter parsed as empty")
        return

    for field in REQUIRED_SKILL_FIELDS:
        if field not in data:
            errors.append(f"[MISSING FIELD] {path}: SKILL.md missing '{field}'")

    effort = data.get("effort", "")
    if effort and effort not in VALID_EFFORTS:
        errors.append(
            f"[INVALID EFFORT] {path}: effort='{effort}' must be one of {VALID_EFFORTS}"
        )

    model = data.get("model", "")
    if model and model not in VALID_MODELS:
        warnings.append(
            f"[UNKNOWN MODEL] {path}: model='{model}' not in known list {VALID_MODELS}"
        )


def check_agent_yaml(path: Path) -> None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        errors.append(f"[YAML ERROR] {path}: {e}")
        return

    if not isinstance(data, dict):
        errors.append(f"[EMPTY FILE] {path}: agent YAML is empty")
        return

    for field in REQUIRED_AGENT_FIELDS:
        if field not in data:
            errors.append(f"[MISSING FIELD] {path}: agent missing '{field}'")


def run_validation(plugin_filter: str | None = None, verbose: bool = False) -> None:
    plugin_dirs = [
        d for d in ROOT.iterdir()
        if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists()
    ]

    if plugin_filter:
        plugin_dirs = [d for d in plugin_dirs if d.name == plugin_filter]

    for plugin_dir in sorted(plugin_dirs):
        if verbose:
            print(f"Checking plugin: {plugin_dir.name}")

        # Check plugin.json
        pjson = plugin_dir / ".claude-plugin" / "plugin.json"
        if pjson.exists():
            check_plugin_json(pjson)

        # Check all SKILL.md files
        for skill_md in plugin_dir.glob("skills/*/SKILL.md"):
            if verbose:
                print(f"  Skill: {skill_md.parent.name}")
            check_skill_md(skill_md)

        # Check agent yaml files
        for agent_yaml in plugin_dir.glob("agents/*.md"):
            if verbose:
                print(f"  Agent: {agent_yaml.name}")
            check_agent_yaml(agent_yaml)

    # Check managed-agent-cookbooks
    cookbooks_dir = ROOT / "managed-agent-cookbooks"
    if cookbooks_dir.exists():
        for agent_yaml in cookbooks_dir.glob("*/agent.yaml"):
            if verbose:
                print(f"Checking cookbook: {agent_yaml.parent.name}")
            check_agent_yaml(agent_yaml)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate claude-for-ca plugin files")
    parser.add_argument("--plugin", help="Validate only this plugin directory name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    run_validation(plugin_filter=args.plugin, verbose=args.verbose)

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print(f"\n❌ {len(errors)} error(s):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"\n✅ Validation passed. {len(warnings)} warning(s), 0 errors.")


if __name__ == "__main__":
    main()
