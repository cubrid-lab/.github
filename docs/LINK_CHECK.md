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

## Adding link-check to a new product repo

1. Drop the caller workflow shown above into `.github/workflows/link-check.yml`.
2. Push to `main` to validate the initial run.
3. (Optional) Add a `lychee.toml` for repo-specific excludes.
4. Once green, the workflow will catch broken links on every Markdown-touching PR.
