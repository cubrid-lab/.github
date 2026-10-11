"""Offline tests for measure_adoption.py (HTTP is mocked).

Run: python -m unittest discover -s scripts -p 'test_*.py'
"""

from __future__ import annotations

import datetime as dt
import io
import json
import sys
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import measure_adoption as ma


class FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, status: int = 200) -> None:
        super().__init__(body)
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def jsonl(rows: list[dict]) -> bytes:
    return "\n".join(json.dumps(r) for r in rows).encode()


CH_ROWS = [
    {"project": "pycubrid", "ci": "false", "is_installer": 0, "downloads": "10"},
    {"project": "pycubrid", "ci": "false", "is_installer": 1, "downloads": "30"},
    {"project": "pycubrid", "ci": "true", "is_installer": 1, "downloads": "60"},
    {"project": "pycubrid", "ci": "unknown", "is_installer": 1, "downloads": "5"},
]


class PypiTests(unittest.TestCase):
    def test_split_by_ci_and_installer(self) -> None:
        captured = {}

        def fake_urlopen(req, timeout):
            captured["url"] = req.full_url
            captured["body"] = req.data.decode()
            return FakeResponse(jsonl(CH_ROWS))

        with mock.patch.object(ma.urllib.request, "urlopen", fake_urlopen):
            out = ma.pypi_downloads(
                ["pycubrid", "cubrid-mcp-server"], dt.date(2026, 9, 1), dt.date(2026, 9, 30)
            )

        self.assertEqual(
            out["pycubrid"],
            {
                "total": 105,
                "ci_true": 60,
                "ci_false": 40,
                "ci_unknown": 5,
                "ci_false_installer": 30,
            },
        )
        # Requested packages with no rows are reported as zero, not dropped.
        self.assertEqual(out["cubrid-mcp-server"]["total"], 0)
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(captured["url"]).query)
        self.assertEqual(qs["user"], ["demo"])
        self.assertEqual(qs["read_overflow_mode"], ["throw"])
        self.assertEqual(qs["param_start"], ["2026-09-01"])
        self.assertEqual(qs["param_projects"], ["['pycubrid','cubrid-mcp-server']"])
        self.assertIn("FROM pypi.pypi", captured["body"])

    def test_array_literal_escapes_quotes(self) -> None:
        self.assertEqual(ma._ch_array(["a'b"]), "['a\\'b']")


class GitHubTests(unittest.TestCase):
    def fake_get(self, path: str):
        if path == "/repos/cubrid-lab/pycubrid":
            return 200, {"stargazers_count": 7, "forks_count": 2}
        if path.startswith("/repos/cubrid-lab/pycubrid/releases"):
            return 200, [{"draft": False}, {"draft": True}, {"draft": False}]
        if path.startswith("/search/issues"):
            return 200, {"total_count": 42}
        if "/traffic/" in path:
            return 403, None
        raise AssertionError(path)

    def test_traffic_403_is_reported_not_fatal(self) -> None:
        gh = ma.GitHub(token=None)
        with mock.patch.object(gh, "get", self.fake_get):
            stats = gh.repo_stats("pycubrid")
        self.assertEqual(stats["stars"], 7)
        self.assertEqual(stats["releases"], 2)  # drafts excluded
        self.assertEqual(stats["merged_prs"], 42)
        self.assertEqual(stats["clones"], "HTTP 403")

        report = ma.render(
            dt.date(2026, 9, 1),
            dt.date(2026, 9, 30),
            "2026-09-30",
            {
                "pycubrid": {
                    "total": 105,
                    "ci_true": 60,
                    "ci_false": 40,
                    "ci_unknown": 5,
                    "ci_false_installer": 30,
                }
            },
            None,
            {"pycubrid": 3},
            {"pycubrid": stats},
            authenticated=False,
        )
        self.assertIn("External downloads 40 (CI excluded)", report)
        self.assertIn("unavailable (HTTP 403)", report)
        self.assertIn("needs push access", report)
        self.assertIn("(30 days, UTC)", report)

    def test_http_error_returns_status(self) -> None:
        err = urllib.error.HTTPError("u", 403, "Forbidden", None, None)
        with mock.patch.object(ma.urllib.request, "urlopen", side_effect=err):
            self.assertEqual(ma.GitHub("t").get("/x"), (403, None))


class MainTests(unittest.TestCase):
    def test_pypi_failure_exits_nonzero(self) -> None:
        with (
            mock.patch.object(ma, "pypi_downloads", side_effect=urllib.error.URLError("down")),
            mock.patch.object(ma, "pypi_release_count", return_value=None),
            mock.patch.object(ma, "github_token", return_value=None),
            mock.patch.object(ma.GitHub, "repo_stats", return_value={}),
            mock.patch("sys.stdout", new_callable=io.StringIO) as out,
        ):
            rc = ma.main(["--window-days", "7", "--end-date", "2026-09-30", "--repos", "pycubrid"])
        self.assertEqual(rc, 1)
        self.assertIn("PyPI query failed", out.getvalue())
        self.assertIn("2026-09-24 to 2026-09-30", out.getvalue())


if __name__ == "__main__":
    unittest.main()
