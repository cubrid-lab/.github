#!/usr/bin/env python3
"""Sync cubrid-lab repo labels from .github/labels.yml (source of truth).

Usage:
  python scripts/sync_labels.py           # apply renames + ensure labels
  python scripts/sync_labels.py --audit   # report drift, change nothing

Requires: gh authenticated with repo scope. Never deletes labels; deletion
stays a human decision surfaced by the audit.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

ORGSPEC = Path(__file__).resolve().parents[1] / ".github" / "labels.yml"
REPOS = ["pycubrid", "sqlalchemy-cubrid", "cubrid-mcp-server", "cubrid-cookbook-python"]


def gh(*args: str) -> dict | list | None:
    out = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if out.returncode != 0:
        return None
    return json.loads(out.stdout) if out.stdout.strip() else None


def labels_of(repo: str) -> dict[str, dict]:
    data = gh(f"repos/cubrid-lab/{repo}/labels?per_page=100") or []
    return {l["name"]: l for l in data}


def ensure(repo: str, existing: dict[str, dict], want: dict) -> None:
    cur = existing.get(want["name"])
    if (
        cur
        and cur.get("color") == want["color"]
        and cur.get("description") == want["description"]
    ):
        return
    if cur:
        done = gh(
            "-X",
            "PATCH",
            f"repos/cubrid-lab/{repo}/labels/{quote(want['name'])}",
            "-f",
            f"color={want['color']}",
            "-f",
            f"description={want['description']}",
        )
        print(f"  {'updated' if done else '!! FAILED'} {want['name']}")
    else:
        done = gh(
            "-X",
            "POST",
            f"repos/cubrid-lab/{repo}/labels",
            "-f",
            f"name={want['name']}",
            "-f",
            f"color={want['color']}",
            "-f",
            f"description={want['description']}",
        )
        print(f"  {'created' if done else '!! FAILED'} {want['name']}")


def rename(repo: str, existing: dict[str, dict], old: str, new: str) -> bool:
    if old not in existing or new in existing:
        return False
    done = gh(
        "-X",
        "PATCH",
        f"repos/cubrid-lab/{repo}/labels/{quote(old)}",
        "-f",
        f"new_name={new}",
    )
    if not done:
        print(f"  !! rename FAILED {old} -> {new}")
        return False
    print(f"  renamed {old} -> {new}")
    return True


def main() -> int:
    spec = yaml.safe_load(ORGSPEC.read_text())
    audit = "--audit" in sys.argv
    core = spec["core"]
    for repo in REPOS:
        print(f"── cubrid-lab/{repo}")
        existing = labels_of(repo)
        if existing == {}:
            print("  !! could not read labels (gh auth?)")
            return 1
        for old, new in spec.get("renames", {}).items():
            if audit:
                if old in existing:
                    print(f"  drift: {old} should be renamed to {new}")
            elif rename(repo, existing, old, new):
                existing.pop(old, None)
                existing[new] = {"name": new, "color": "", "description": ""}
        repo_spec = spec.get("repos", {}).get(repo, {})
        for old, new in repo_spec.get("area_renames", {}).items():
            if audit:
                if old in existing:
                    print(f"  drift: {old} should be renamed to {new}")
            elif rename(repo, existing, old, new):
                existing.pop(old, None)
                existing[new] = {"name": new, "color": "", "description": ""}
        wanted = list(core) + repo_spec.get("areas", [])
        for want in wanted:
            if audit:
                cur = existing.get(want["name"])
                if not cur:
                    print(f"  missing: {want['name']}")
                elif (
                    cur["color"] != want["color"]
                    or cur["description"] != want["description"]
                ):
                    print(f"  mismatch: {want['name']}")
            else:
                ensure(repo, existing, want)
        if audit:
            known = {w["name"] for w in wanted} | set(spec.get("renames", {}))
            for name in existing:
                if name not in known:
                    print(
                        f"  extra: {name} (not in spec — delete manually if obsolete)"
                    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
