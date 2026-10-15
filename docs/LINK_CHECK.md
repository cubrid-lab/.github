# Link Checker

This repository provides a reusable [lychee](https://github.com/lycheeverse/lychee)-based link checker workflow that all cubrid-lab product repos can consume.

## Usage

Add a caller workflow at `.github/workflows/link-check.yml` in any cubrid-lab product repo (pycubrid, sqlalchemy-cubrid, cubrid-cookbook-python, etc.):

```yaml
name: link-check
on:
  push:
    paths:
      - "**/*.md"
  pull_request:
    paths:
      - "**/*.md"
  schedule:
    - cron: "0 6 * * 1"

jobs:
  check:
    uses: cubrid-lab/.github/.github/workflows/link-check.yml@main
    with:
      fail-on-error: true
      files: "*.md docs/**/*.md"
```

## Behavior

| Trigger        | Behavior                                                           |
|----------------|--------------------------------------------------------------------|
| PR / push      | Fails the build if broken Markdown links are found                 |
| Weekly schedule| Opens an issue listing broken links (does not fail the run silently)|
| `workflow_dispatch` | Manual run from the Actions tab                                |

## Defaults

- Excludes `localhost`, `127.0.0.1`, and `example.com` URLs
- Default file patterns: `*.md docs/**/*.md`
- Per-repo `lychee.toml` at the repo root overrides these defaults

## Configuration

Product repos may add a `lychee.toml` at the root for additional excludes or headers. See the [lychee configuration docs](https://github.com/lycheeverse/lychee#configuration) for the full schema.

Example `lychee.toml`:

```toml
exclude = [
  "https://codecov\\.io/.*",
  "https://img\\.shields\\.io/.*",
]
exclude_path = ["./vendor", "./node_modules"]
```

## Pull-request link check in `doc-lint.yml`

The reusable `doc-lint.yml` workflow (Markdown style, links, Mermaid) runs its own
lychee job on pull requests. It checks local file links in every `*.md` file and
skips `http(s)://` URLs unless `check-external-links: true`; this weekly
`link-check.yml` workflow checks external URLs.

| Outcome | `fail-on-issue: false` | `fail-on-issue: true` |
|---|---|---|
| No broken links | Pass | Pass |
| Broken or timed-out links (lychee exit 2) | Pass, with a warning annotation per link and a job-summary table | Fail, with an error annotation per link |
| lychee failed: invalid argument, invalid `lychee.toml`, crash, or any exit code other than 0 or 2 | **Fail** | **Fail** |

A completed run exits 0 or 2 and writes a JSON report; anything else, or a
missing report, is a tool or configuration error. The exit code alone is not
enough (2 means both "invalid argument" and "rejected link"), and neither is the
report alone (lychee can still fail after writing it, while saving its cache).
Timeouts count as rejected links unless the caller's `lychee.toml` sets
`accept_timeouts`. The lychee version is pinned
(`lycheeVersion: v0.24.2`), so an upstream release cannot remove an option the
workflow passes; v0.24.2 removed `--exclude-mail`, which made every earlier run stop
before checking a link while the job still reported success (#54). Each
comma-separated `exclude` entry becomes its own `--exclude-path` regular
expression. `doc-lint-self-test.yml` runs the workflow on this repository whenever
it changes.

## Adding link-check to a new product repo

1. Drop the caller workflow shown above into `.github/workflows/link-check.yml`.
2. Push to `main` to validate the initial run.
3. (Optional) Add a `lychee.toml` for repo-specific excludes.
4. Once green, the workflow will catch broken links on every Markdown-touching PR.
