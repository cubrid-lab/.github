#!/usr/bin/env python3
"""Check the organization profile (profile/README.md) for facts that go stale.

Fails (exit 1) when:
  * a table row in the "## Projects" section states a hard-coded version
    (``v<digits>.<digits>.<digits>``) instead of a live badge;
  * a repository listed in those tables is missing, archived or renamed;
  * a public, non-fork, non-archived cubrid-lab repository is not listed
    (except the ones in UNLISTED_OK).

Usage:
  python scripts/check_profile_drift.py [--readme PATH] [--offline] [--report FILE]

--offline runs only the version check (no GitHub API calls).
GITHUB_TOKEN or GH_TOKEN, when set, authenticates the API calls.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG = "cubrid-lab"
README = Path(__file__).resolve().parents[1] / "profile" / "README.md"
# Public repositories that intentionally have no row in the Projects tables.
UNLISTED_OK = {".github", "cubrid-lab.github.io"}
VERSION_RE = re.compile(r"\bv\d+\.\d+\.\d+\b")
REPO_CELL_RE = re.compile(rf"^\|\s*\*\*\[[^\]]+\]\(https://github\.com/{ORG}/([^/)\s]+)\)\*\*")


def projects_rows(text: str) -> list[tuple[int, str]]:
    """Return (line number, line) for every table row in the Projects section."""
    rows: list[tuple[int, str]] = []
    inside = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            inside = line.strip() == "## Projects"
            continue
        if inside and line.startswith("|"):
            rows.append((number, line))
    return rows


def api(path: str) -> tuple[int, object]:
    request = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-drift"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return 404, None
        raise


def org_public_repos() -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        _, data = api(f"orgs/{ORG}/repos?type=public&per_page=100&page={page}")
        assert isinstance(data, list)
        repos.extend(data)
        if len(data) < 100:
            return repos
        page += 1


def check(text: str, offline: bool) -> list[str]:
    problems: list[str] = []
    listed: list[str] = []
    for number, line in projects_rows(text):
        for version in VERSION_RE.findall(line):
            problems.append(
                f"line {number}: hard-coded version `{version}` in a Projects table "
                "(use a live release badge)"
            )
        match = REPO_CELL_RE.match(line)
        if match:
            listed.append(match.group(1))

    if not listed:
        problems.append("no repository rows found in the Projects section")
    if offline:
        return problems

    for name in listed:
        status, repo = api(f"repos/{ORG}/{name}")
        if status == 404 or not isinstance(repo, dict):
            problems.append(f"`{ORG}/{name}` is listed but does not exist")
            continue
        if repo["full_name"] != f"{ORG}/{name}":
            problems.append(f"`{ORG}/{name}` is listed but was renamed to `{repo['full_name']}`")
        if repo.get("archived"):
            problems.append(f"`{ORG}/{name}` is listed but is archived")

    known = set(listed) | UNLISTED_OK
    for repo in org_public_repos():
        if repo["fork"] or repo["archived"] or repo["name"] in known:
            continue
        problems.append(f"public repository `{ORG}/{repo['name']}` is not listed in Projects")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--readme", type=Path, default=README)
    parser.add_argument("--offline", action="store_true", help="skip GitHub API checks")
    parser.add_argument("--report", type=Path, help="write a Markdown report to this file")
    args = parser.parse_args()

    problems = check(args.readme.read_text(encoding="utf-8"), args.offline)
    if problems:
        report = "The organization profile states facts that are out of date:\n\n"
        report += "".join(f"- {problem}\n" for problem in problems)
    else:
        report = "The organization profile matches the current repositories.\n"
    print(report, end="")
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
