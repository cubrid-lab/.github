# cubrid-lab Conventions & Operations Manual

How the four Python ecosystem repos (pycubrid, sqlalchemy-cubrid,
cubrid-mcp-server, cubrid-cookbook-python) are released, verified, and
maintained. Everything here was learned the hard way — treat it as binding.

## Roles

- **Maintainers**: Yeongseon Choe, Gyeongjun Paik — review, release gates, labels that promise mentoring.
- **AI agent** (`sisyphus-dev-ai`): implementation via PRs under AGENTS.md rules; never pushes release tags or publishes.
- **Release act is human**: a human pushes the `vX.Y.Z` tag (or dispatches the publish workflow) after review.

## Release process (per package repo)

1. PR: version bump + `CHANGELOG.md` dated section (`scripts/lint_changelog.py` enforces format) — merge to `main`.
2. PyPI **Pending Publisher** must be registered once per project (owner `cubrid-lab`, workflow `publish-pypi.yml`, environment `pypi`).
3. Human pushes the tag: `git tag vX.Y.Z <merged main SHA> && git push origin vX.Y.Z`.
4. `create-release.yml` extracts release notes from the CHANGELOG section (fail-closed; no generated-notes fallback), creates the **published** GitHub Release, generates and uploads `sbom.spdx.json` as a release asset.
5. Publishing triggers `publish-pypi.yml` (Trusted Publishing / OIDC, environment `pypi`). ⚠️ If the release was created **by a workflow using GITHUB_TOKEN, the `release: published` event does NOT trigger other workflows** (recursion guard) — re-run publish via `workflow_dispatch` with the tag input instead.
6. `notify-cookbook.yml` dispatches `upstream-released` to cubrid-cookbook-python for dogfood smoke (needs the `COOKBOOK_DISPATCH_TOKEN` secret; currently pending registration).

Known gotchas (both fixed in the workflows, kept here as memory):
- `gh release create --target <tag>` on an **existing tag** returns HTTP 422 — `--verify-tag` alone is correct.
- Version gates in publish-pypi: tag must equal `v$VERSION`, CHANGELOG must contain the dated section, tag must be an ancestor of `main`.

## Docs sites (cubrid-lab.github.io/<repo>)

- All four repos run mkdocs-material sites with the **same six-tab IA**:
  `Home / Getting Started / Usage / Reference / Operations / Project`,
  blue palette, `search.suggest`, translations under `Project → Translations`.
- Build is strict: `mkdocs build --strict` in `docs.yml` (deploy on push to `main`; Pages must be enabled with the *GitHub Actions* source, `build_type=workflow`).
- **cookbook**: site pages are staged from repo-root sources by `scripts/stage_docs.sh`
  (run by CI and `make docs`; staged files are gitignored) — the repo stays the single source of truth.
- Every homepage links the other three sites (Ecosystem section). Sibling READMEs cross-link via Related Projects.

## CI gates and escape hatches

| Gate | Workflow / job | Blocks on | Escape hatch |
|---|---|---|---|
| Docs sync | `docs-sync` | behavior change without README/CHANGELOG/docs update | `docs-not-needed` label or `Docs: not needed - <reason>` in PR body |
| Translation sync | `translation-sync` (in docs-sync) | `README.md` changed without `docs/README.ko.md` (한국어 is required until the 2026 contest finals; de/hi/ru/zh warn only) | `translations-deferred` label |
| Changelog lint | mcp-server `ci.yml` | missing/undated `[Unreleased]`/version sections | none (fix the changelog) |
| Integration matrices | pycubrid/sqlalchemy (Python × CUBRID 10.2–11.4), mcp-server (CUBRID 11.2+11.4), cookbook smoke (`make verify` goldens, 11.2+11.4) | live-DB test failure | none; infra flakes → re-run |
| CI gate / matrix-result | summary jobs | any leg failed | none |

Runner-port flakes (`address already in use` on 33000) are re-runs, not code problems.

## Labels

Source of truth: [`.github/labels.yml`](.github/labels.yml) · sync: `python scripts/sync_labels.py` · weekly drift audit: `label-audit` workflow (needs `LABEL_AUDIT_TOKEN`, read-only, deletion stays a human call). Rules: spaced-colon prefixes, escape-hatch labels share one color, `good first issue` / `help wanted` are maintainer promises (never auto-applied). See the table in [CONTRIBUTING.md](CONTRIBUTING.md).

## Translations

Policy in [AGENTS.md](AGENTS.md#translation-policy-cubrid-lab-org): English canonical; 한국어 required-to-sync (hard gate, time-boxed for the contest — relax after 2026 finals, see the reminder issue); de/hi/ru/zh community translations with advisory drift warnings and maintainer-side resync PRs. Every translated file carries a sync marker blockquote.

## Licensing & attribution (verified 2026-09)

- All four repos: **MIT**, copyright `Yeongseon Choe, Gyeongjun Paik` (year range per repo start).
- `THIRD_PARTY_LICENSES.md` + `NOTICE` in every repo. No GPL anywhere in runtime or dev trees.
- **CUBRID server is Apache-2.0 (engine) / BSD (APIs & connectors)** per upstream `COPYING` — the often-cited "GPL v2+" is outdated; our repos state this accurately and note we are independent wire-protocol clients, with `cubrid/cubrid` Docker images used for CI/demo only.
- Releases carry SPDX SBOM assets (`sbom.spdx.json`).

## Secrets inventory

| Secret | Where | Purpose | Status |
|---|---|---|---|
| (PyPI Trusted Publisher) | PyPI project settings | OIDC publish, no token | registered per project at first release — mcp-server was blocked on it (#154) |
| `COOKBOOK_DISPATCH_TOKEN` | cubrid-mcp-server | cross-repo `upstream-released` dispatch | pending |
| `LABEL_AUDIT_TOKEN` | cubrid-lab/.github | weekly label drift audit (read) | pending |

## Lessons encoded in tooling

- Golden outputs (cookbook `expected/*.expected`) record behavior of the *tested* stack — when a driver fix changes output, regenerate the goldens from the corrected behavior and say so in the changelog.
- Workflow files are kept identical across the three package repos ("canonical publish workflow") — change one, port to all three in the same PR.
- `upstream-canary.yml` (mcp-server) tracks `pycubrid@main` **and** `fastmcp@latest`; dependency pins (e.g. `fastmcp>=3.0,<4`) only open after the canary is green.
