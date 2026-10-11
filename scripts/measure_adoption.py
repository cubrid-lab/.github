#!/usr/bin/env python3
"""Measure cubrid-lab adoption with self-generated CI traffic separated out.

Usage:
  python scripts/measure_adoption.py                      # 30-day window, print report
  python scripts/measure_adoption.py --window-days 14 --output report.md

Sources (standard library only, no secrets):
  * PyPI downloads: the public ClickHouse mirror of PyPI's download log
    (https://sql-clickhouse.clickhouse.com, read-only ``demo`` user). Its
    event-level table ``pypi.pypi`` keeps linehaul's ``ci`` column
    (``true`` / ``false`` / ``unknown``), which the per-day summary tables drop.
  * GitHub: REST API (stars, forks, releases, merged PRs, and Traffic API
    clones/views). Uses GH_TOKEN / GITHUB_TOKEN, else ``gh auth token`` if gh
    is installed. Traffic needs push access; a 403 is reported, not fatal.

The ``ci`` flag is the installer's self-report (pip/uv detect CI environment
variables). It is not ground truth; see docs/METRICS_SNAPSHOT.md for caveats.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

CLICKHOUSE_URL = "https://sql-clickhouse.clickhouse.com/"
GITHUB_API = "https://api.github.com"
ORG = "cubrid-lab"
# PEP 503 normalized names: the download log stores only these spellings.
PACKAGES = ["pycubrid", "sqlalchemy-cubrid", "cubrid-mcp-server"]
REPOS = ["pycubrid", "sqlalchemy-cubrid", "cubrid-mcp-server", "cubrid-cookbook-python"]
# Real package installers. Everything else with ci=false (mirrors such as
# bandersnatch/Nexus, browsers, plain HTTP clients, empty user agent) is
# reported separately as "mirror / other".
INSTALLERS = ["pip", "uv", "poetry", "pdm", "pipenv"]
TIMEOUT = 60

PYPI_QUERY = """
SELECT
    project,
    toString(ci) AS ci,
    installer IN {installers:Array(String)} AS is_installer,
    count() AS downloads
FROM pypi.pypi
WHERE project IN {projects:Array(String)}
  AND date BETWEEN {start:Date} AND {end:Date}
GROUP BY project, ci, is_installer
ORDER BY project, ci, is_installer
FORMAT JSONEachRow
"""

LATEST_QUERY = """
SELECT toString(max(date)) AS latest
FROM pypi.pypi
WHERE project IN {projects:Array(String)} AND date >= {start:Date}
FORMAT JSONEachRow
"""


def _ch_array(values: list[str]) -> str:
    return (
        "["
        + ",".join("'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'" for v in values)
        + "]"
    )


def clickhouse(query: str, params: dict[str, str]) -> list[dict]:
    """Run a read-only query on the public ClickHouse endpoint."""
    qs = {"user": "demo", "read_overflow_mode": "throw"}
    qs.update({f"param_{k}": v for k, v in params.items()})
    req = urllib.request.Request(
        CLICKHOUSE_URL + "?" + urllib.parse.urlencode(qs),
        data=query.encode(),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        body = resp.read().decode()
    return [json.loads(line) for line in body.splitlines() if line.strip()]


def pypi_downloads(packages: list[str], start: dt.date, end: dt.date) -> dict[str, dict[str, int]]:
    """Return per-package counts: total, ci_true, ci_false, ci_unknown, ci_false_installer."""
    rows = clickhouse(
        PYPI_QUERY,
        {
            "projects": _ch_array(packages),
            "installers": _ch_array(INSTALLERS),
            "start": start.isoformat(),
            "end": end.isoformat(),
        },
    )
    keys = ("total", "ci_true", "ci_false", "ci_unknown", "ci_false_installer")
    out = {p: dict.fromkeys(keys, 0) for p in packages}
    for row in rows:
        stats = out.setdefault(row["project"], dict.fromkeys(keys, 0))
        n = int(row["downloads"])
        stats["total"] += n
        stats[f"ci_{row['ci']}"] += n
        if row["ci"] == "false" and int(row["is_installer"]):
            stats["ci_false_installer"] += n
    return out


def latest_pypi_date(packages: list[str], start: dt.date) -> str | None:
    rows = clickhouse(LATEST_QUERY, {"projects": _ch_array(packages), "start": start.isoformat()})
    latest = rows[0]["latest"] if rows else None
    return None if latest in (None, "1970-01-01") else latest


def pypi_release_count(package: str) -> int | None:
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=TIMEOUT) as r:
            return len(json.load(r).get("releases", {}))
    except (urllib.error.URLError, ValueError):
        return None


def github_token() -> str | None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    if shutil.which("gh"):
        # `gh auth token` needs gh >= 2.17; older releases expose it via config.
        for cmd in (["auth", "token"], ["config", "get", "-h", "github.com", "oauth_token"]):
            out = subprocess.run(["gh", *cmd], capture_output=True, text=True, check=False)
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip()
    return None


class GitHub:
    def __init__(self, token: str | None) -> None:
        self.token = token

    def get(self, path: str) -> tuple[int, object]:
        """GET a REST path; return (status, json body or None)."""
        req = urllib.request.Request(GITHUB_API + path)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.status, json.load(resp)
        except urllib.error.HTTPError as err:
            return err.code, None

    def count_releases(self, full: str) -> int | None:
        """Count published (non-draft) releases; drafts are visible only with push access."""
        total, page = 0, 1
        while True:
            status, body = self.get(f"/repos/{full}/releases?per_page=100&page={page}")
            if status != 200 or not isinstance(body, list):
                return None
            total += sum(1 for rel in body if not rel.get("draft"))
            if len(body) < 100:
                return total
            page += 1

    def repo_stats(self, repo: str) -> dict[str, object]:
        full = f"{ORG}/{repo}"
        stats: dict[str, object] = {}
        status, body = self.get(f"/repos/{full}")
        if status == 200 and isinstance(body, dict):
            stats["stars"] = body.get("stargazers_count")
            stats["forks"] = body.get("forks_count")
        stats["releases"] = self.count_releases(full)
        q = urllib.parse.quote(f"repo:{full} is:pr is:merged")
        status, body = self.get(f"/search/issues?q={q}&per_page=1")
        stats["merged_prs"] = (
            body.get("total_count") if status == 200 and isinstance(body, dict) else None
        )
        for kind in ("clones", "views"):
            status, body = self.get(f"/repos/{full}/traffic/{kind}")
            if status == 200 and isinstance(body, dict):
                stats[kind] = (body.get("count"), body.get("uniques"))
            else:
                stats[kind] = f"HTTP {status}"
        return stats


def _fmt(value: object) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def _pct(part: int, whole: int) -> str:
    return f"{100 * part / whole:.1f}%" if whole else "n/a"


def render(
    start: dt.date,
    end: dt.date,
    latest: str | None,
    downloads: dict[str, dict[str, int]] | None,
    pypi_error: str | None,
    releases: dict[str, int | None],
    github: dict[str, dict[str, object]],
    authenticated: bool,
) -> str:
    days = (end - start).days + 1
    lines = [
        "# cubrid-lab adoption report",
        "",
        f"- Generated: {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC",
        f"- PyPI window: {start} to {end} ({days} days, UTC)",
        f"- Latest PyPI log date available: {latest or 'unknown'}",
        "- PyPI source: ClickHouse public mirror, table `pypi.pypi`, column `ci`",
        "",
        "## PyPI downloads",
        "",
    ]
    if downloads is None:
        lines += [f"PyPI query failed: {pypi_error}", ""]
    else:
        lines += [
            (
                "| Package | All (CI included) | ci=true | ci=false | ci=unknown | CI share "
                "| ci=false via installers | ci=false mirror / other | PyPI releases |"
            ),
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        tot = dict.fromkeys(("total", "ci_true", "ci_false", "ci_unknown", "ci_false_installer"), 0)
        for pkg, s in downloads.items():
            for k in tot:
                tot[k] += s[k]
            lines.append(
                f"| {pkg} | {s['total']:,} | {s['ci_true']:,} | {s['ci_false']:,} "
                f"| {s['ci_unknown']:,} | {_pct(s['ci_true'], s['total'])} "
                f"| {s['ci_false_installer']:,} | {s['ci_false'] - s['ci_false_installer']:,} "
                f"| {_fmt(releases.get(pkg))} |"
            )
        lines.append(
            f"| **Total** | **{tot['total']:,}** | **{tot['ci_true']:,}** | **{tot['ci_false']:,}** "
            f"| **{tot['ci_unknown']:,}** | **{_pct(tot['ci_true'], tot['total'])}** "
            f"| **{tot['ci_false_installer']:,}** "
            f"| **{tot['ci_false'] - tot['ci_false_installer']:,}** "
            f"| **{_fmt(sum(v for v in releases.values() if v))}** |"
        )
        lines += [
            "",
            (
                f"External downloads {tot['ci_false']:,} (CI excluded); "
                f"of which {tot['ci_false_installer']:,} came from package installers "
                f"({', '.join(INSTALLERS)})."
            ),
            "",
            "Notes: `ci` is self-reported by the installer. `ci=false` still includes",
            "maintainers' local installs and mirror syncs; the installer column removes",
            "mirrors, browsers and bare HTTP clients. `ci=unknown` is shown, not folded in.",
            "",
        ]

    lines += [
        "## GitHub",
        "",
        (
            "| Repository | Stars | Forks | Releases | Merged PRs "
            "| Clones 14d (total / unique) | Views 14d (total / unique) |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    traffic_denied = False
    for repo, s in github.items():
        cells = []
        for kind in ("clones", "views"):
            v = s.get(kind)
            if isinstance(v, tuple):
                cells.append(f"{_fmt(v[0])} / {_fmt(v[1])}")
            else:
                traffic_denied = True
                cells.append(f"unavailable ({v})")
        lines.append(
            f"| {repo} | {_fmt(s.get('stars'))} | {_fmt(s.get('forks'))} "
            f"| {_fmt(s.get('releases'))} | {_fmt(s.get('merged_prs'))} | {cells[0]} | {cells[1]} |"
        )
    lines.append("")
    if traffic_denied:
        lines += [
            "Traffic API (clones/views) needs push access to the repository; it was not",
            "available with the current credentials"
            + ("." if authenticated else " (no token found)."),
            "",
        ]
    lines += [
        "Clones and views cover the last 14 days only. Clones are NOT CI-free:",
        "`actions/checkout` runs `git fetch` when git is on the runner (all GitHub-hosted",
        "runners), and the Traffic API cannot separate CI from people.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--window-days", type=int, default=30, help="PyPI window length (default 30)")
    ap.add_argument(
        "--end-date",
        type=dt.date.fromisoformat,
        default=None,
        help="last day of the window, YYYY-MM-DD (default: yesterday, UTC)",
    )
    ap.add_argument("--output", help="write the markdown report to this file instead of stdout")
    ap.add_argument("--packages", nargs="+", default=PACKAGES, help="PyPI projects (normalized)")
    ap.add_argument("--repos", nargs="+", default=REPOS, help=f"repositories under {ORG}")
    args = ap.parse_args(argv)
    if args.window_days < 1:
        ap.error("--window-days must be >= 1")

    end = args.end_date or (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1))
    start = end - dt.timedelta(days=args.window_days - 1)

    downloads, pypi_error, latest = None, None, None
    try:
        downloads = pypi_downloads(args.packages, start, end)
        latest = latest_pypi_date(args.packages, start)
    except (urllib.error.URLError, ValueError, KeyError) as err:
        pypi_error = str(err)
    releases = {p: pypi_release_count(p) for p in args.packages}

    token = github_token()
    gh = GitHub(token)
    github = {repo: gh.repo_stats(repo) for repo in args.repos}

    report = render(start, end, latest, downloads, pypi_error, releases, github, bool(token))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(report)
    return 0 if downloads is not None else 1


if __name__ == "__main__":
    sys.exit(main())
