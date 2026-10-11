# Adoption metrics snapshot — for presentations

> Measured: 2026-10-11 (UTC) with [`scripts/measure_adoption.py`](../scripts/measure_adoption.py).
> PyPI window: **2026-09-11 to 2026-10-10 (30 days)**. GitHub traffic: last 14 days as reported
> by the Traffic API on 2026-10-11.

## Headline numbers

Use the CI-excluded figures on slides. The CI-inclusive figures are shown only so the
difference is visible.

| Metric | pycubrid | sqlalchemy-cubrid | cubrid-mcp-server | cubrid-cookbook-python | **Total** |
|---|---:|---:|---:|---:|---:|
| PyPI downloads, 30d, **CI excluded** (`ci=false`) | 6,080 | 5,117 | 738 | — | **11,935** |
| of which via pip / uv / poetry / pdm / pipenv | 4,071 | 3,180 | 35 | — | **7,286** |
| PyPI downloads, 30d, CI included (all rows) | 20,430 | 13,926 | 872 | — | 35,228 |
| Share of downloads flagged CI (`ci=true`) | 70.2% | 63.3% | 15.4% | — | 66.1% |
| PyPI releases | 20 | 23 | 1 | — | **44** |
| GitHub stars | 31 | 38 | 32 | 28 | **129** |
| GitHub forks | 18 | 14 | 8 | 9 | **49** |
| GitHub releases (published) | 24 | 21 | 5 | 0 | **50** |
| Merged PRs | 406 | 388 | 137 | 138 | **1,069** |
| Unique visitors, 14d | 53 | 44 | 13 | 20 | **130** |
| Unique cloners, 14d (**CI included**, see below) | 1,562 | 1,390 | 381 | 621 | 3,954 |
| Active CI workflows | 22 | 22 | 12 | 12 | **68** |
| Docs site (HTTP 200) | yes | yes | yes | yes | **4/4** |

Suggested slide labels:

- "External downloads **11,935** in 30 days (CI excluded)"
- Conservative variant: "**7,286** downloads via pip/uv/poetry in 30 days (CI and mirrors excluded)"

## How CI traffic is excluded

PyPI's download log (linehaul) records whether the installer reported running in CI. The
public ClickHouse mirror keeps that column on its event-level table `pypi.pypi`:

```text
ci  Enum8('false' = 0, 'true' = 1, 'unknown' = 2)
```

(verified with `DESCRIBE TABLE pypi.pypi` on 2026-10-11). The per-day summary tables drop it,
so the script queries the event-level table directly. No account or key is needed. This
replaces the originally planned approach of rebuilding the CI split from GitHub Actions IP
ranges in BigQuery.

Columns in the report:

- **`ci=true`**: the installer said it ran in CI (pip and uv detect CI environment variables).
  Our own CI (cookbook smoke tests, pycubrid / sqlalchemy-cubrid integration matrices) lands here.
- **`ci=false`**: everything else that did not report CI. This is the "CI excluded" figure.
- **`ci=unknown`**: neither. It was 0 for all three packages in this window; the script
  reports it separately instead of folding it into either side.
- **via installers**: the `ci=false` rows whose user agent is pip, uv, poetry, pdm or pipenv.
  The remainder ("mirror / other") is mirrors such as bandersnatch and Nexus, browsers, plain
  HTTP clients and an empty user agent.

The 14-day picture is more CI-heavy (PR activity was high): 26,522 downloads in total, of which
19,597 (73.9%) were `ci=true`; 6,925 CI excluded, 3,913 via installers.

## Caveats (state these if asked)

1. **The `ci` flag is self-reported** by the installer. It is not ground truth; a runner that
   does not set the usual environment variables is counted as `ci=false`.
2. **CI excluded is not "unique users".** `ci=false` still includes maintainers' local installs,
   repeated installs by the same person, and mirror syncs. The installer-only figure removes
   mirrors but not repeats.
3. **cubrid-mcp-server** has few installer downloads (35 of 738 `ci=false`); most of its
   traffic is mirrors. Its first PyPI release is recent, so its numbers are not comparable yet.
4. **GitHub clones are not CI-free.** The earlier assumption that `actions/checkout` uses the
   tarball API and is therefore excluded from clone counts is wrong: `actions/checkout` only
   falls back to the REST API when Git 2.18+ is missing, and GitHub-hosted runners ship Git.
   With roughly 900 to 2,500+ workflow runs per repository in 14 days, unique-cloner counts
   are dominated by CI and cannot be split with the Traffic API. Do not present clones as
   developer interest.
   Unique visitors (views) are the safer GitHub traffic signal.
5. Package names must be PEP 503 normalized (`sqlalchemy-cubrid`, not `sqlalchemy_cubrid`);
   a zero from this dataset is often a spelling mistake, not an absence.
6. The ClickHouse mirror lags PyPI by about a day; the report prints the latest download event
   date for the selected packages (a quiet package can show an earlier date than the mirror).
   The endpoint is queried with `read_overflow_mode=throw` so an oversized scan fails instead
   of silently returning a partial count.

## Re-measuring

```bash
# Full report (PyPI split + GitHub stats), 30-day window ending yesterday (UTC)
python scripts/measure_adoption.py --window-days 30 --output adoption.md

# Reproduce this snapshot exactly
python scripts/measure_adoption.py --window-days 30 --end-date 2026-10-10

# Unit tests (mocked HTTP, no network)
python -m unittest discover -s scripts -p 'test_*.py'
```

GitHub numbers use `GH_TOKEN` / `GITHUB_TOKEN`, or the token of a logged-in `gh` CLI. Clone and
view counts need push access to each repository; without it the report says "unavailable
(HTTP 403)" (or 401 without a token) and continues.

The raw PyPI query, runnable by anyone at
`https://sql-clickhouse.clickhouse.com/?user=demo&read_overflow_mode=throw`:

```sql
SELECT project, ci, count() AS downloads
FROM pypi.pypi
WHERE project IN ('pycubrid', 'sqlalchemy-cubrid', 'cubrid-mcp-server')
  AND date BETWEEN toDate('2026-09-11') AND toDate('2026-10-10')
GROUP BY project, ci
ORDER BY project, ci
```

Active workflows and docs sites are not in the script; they were checked with:

```bash
gh api repos/cubrid-lab/pycubrid/actions/workflows --jq '[.workflows[]|select(.state=="active")]|length'
curl -s -o /dev/null -w '%{http_code}' -L https://cubrid-lab.github.io/pycubrid/
```

## Known gaps

| Metric | Status | Direction |
|---|---|---|
| Unique users | Not measurable from PyPI | Downloads are events, not people |
| GitHub clones without CI | Not measurable | Use unique visitors instead |
| External contributors | Not re-measured (2 on 2026-09-12) | Seed good first issues |
| Fork ratio | Low | Users install from PyPI rather than fork |

## Before the presentation

- [ ] One week before: re-run the script and update this file.
- [ ] Morning of the presentation: final re-run; copy the "CI excluded" line onto the slide.
- [ ] If CUBRID official listing is confirmed: add a "sponsor recognition" row.

---
*Kept in cubrid-lab/.github and maintained at the organization level.*
