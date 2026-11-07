# Change-impact-based CI policy

This standard applies to every active CUBRID Lab repository. It describes the
**outcome** that must be preserved, not one shared workflow implementation. Each
repository owns its own language-specific jobs, dependencies, runtime versions,
and security/release gates.

## Principle

Run the smallest **sufficient** set of checks on pull requests. A documentation
change must not start a live database just because a nearby Python script or CI
configuration directory uses a broad glob. Conversely, an uncertain or
misclassified path must never silently suppress required compatibility tests.

## Change-impact categories

| Category | Examples | PR validation |
| --- | --- | --- |
| Documentation | README, CHANGELOG, docs text/images | Changed documentation, links and formatting; MkDocs build if affected |
| Release automation | changelog composer, contributor attribution, release-note validator, release-please wiring | Targeted automation tests, release workflow contracts, notes formatting |
| Repository tooling | CI check scripts, site generators, automation metadata | Targeted tooling tests; build/safety jobs if directly affected |
| Runtime / API | Python dialect/driver, Rust/Go/TS production source | Language-specific lint, type checks, relevant unit and compatibility tests |
| Database integration | driver protocol, transaction and DB fixtures, live harness | Relevant CUBRID live integration and regression checks |
| Dependencies and build | lockfiles, module files, compiler/runtime configuration | Version/packaging compatibility and affected runtime lanes |
| CI impact classifier | classifier itself, shared decision tables, required result gate | Conservative self-test, typically full validation |
| Unknown / incomplete | unknown path, unavailable diff, deleted/renamed files not assessed | Fail closed to the wider validation tier |

Categories may overlap: a PR touching both documentation and runtime selects
both sets of checks. Pure release-tooling changes need not select a live DB
suite unless that tooling controls database execution or the release gate.

## Required safety properties

1. **Correct PR diff:** use the actual tested PR merge or API file list;
   handle pagination, binary paths, renames (old *and* new names), deleted files,
   and an unavailable API. On uncertainty, run full validation.
2. **Required status:** preserve a stable, always-reported aggregate gate or
   equivalent required status that evaluates *selected* job outcomes.
   A required but intentionally skipped matrix job must not strand a PR in
   Pending. Change branch protection only with a separately reviewed,
   repository-specific migration.
3. **Failure handling:** a required job that fails, is cancelled, is skipped
   unexpectedly, or never starts cannot be treated as success.
4. **Self-test:** include representative path fixtures for documentation,
   release scripts, workflow edits, runtime, dependencies, DB harnesses,
   mixed changes, renamed/deleted files, and unknown paths. Test the matcher
   actually used by the workflow, not an unrelated approximation.
5. **Main and release safety:** do not weaken protected `main` pushes,
   publication gates, scheduled deep checks, release assets, attestations,
   credentials, or required security scans merely to reduce PR runner time.
6. **Least privilege:** the classifier should not receive release secrets,
   cloud credentials, write permission, or access to privileged runners.
   Do not evaluate untrusted PR scripts with elevated tokens.
7. **Observability:** publish a short job summary identifying selected and
   omitted lanes and the reason. Review runner **job-minutes** and queue time
   before and after; a visually skipped check is not necessarily a costly job.
8. **Review before merge:** path-selection workflows need an independent
   review of false-negative risks and status-check compatibility.

## Representative acceptance table

| Changed files on PR | Documentation | Targeted tooling | Runtime | Live DB |
| --- | --- | --- | --- | --- |
| `README.md` | Yes | No | No | No |
| `CHANGELOG.md`, `docs/releases/v*.md` | Yes | Note format as needed | No | No |
| Release-note annotation script and its tests | Yes if notes affected | Yes | No | No |
| Dialect, protocol, connection or transaction implementation | As needed | As needed | Yes | Yes where applicable |
| Integration test harness or database fixture | As needed | Yes | Yes if affected | Yes |
| Dependency lockfile | As needed | As needed | Yes | Where compatibility risk requires |
| Impact-classifier/required gate | As needed | Yes | Conservative/full | Conservative/full |
| Mixed README + runtime | Yes | As needed | Yes | As required |
| Unknown, inaccessible or ambiguous diff | Yes if uncertain | Yes | Yes | Yes for DB-capable repositories |

Repositories without a live database job should treat the Live DB column as
not applicable, rather than starting a remote service.

## Language-specific examples

- Python packages: use repository-tooling tests to validate release-note
  scripts; avoid running the CUBRID protocol/dialect matrix for notes only.
- Node.js packages: keep the supported Node matrix for source and package
  metadata, but use a lightweight docs/release-note gate for Markdown edits.
- Go/Rust drivers: preserve real DB integration for relevant runtime changes;
  a docs-only PR can run format/link checks without container services.
- Kubernetes Operator: use workflow-specific impact decisions; keep the
  fail-closed fallback and HA safety evidence.
- Terraform infrastructure: a docs-only PR must not reach a secret-backed
  Terraform plan. Unknown or state/backend changes still require planning.

## Rollout and ownership

Keep implementation issues and PRs in the **repository being changed**, not
in the organization policy repository. The umbrella audit is
[cubrid-lab/.github#74](https://github.com/cubrid-lab/.github/issues/74).

Roll out one repository at a time:
1. Read the current workflow, branch-protection expectations and recent jobs.
2. Add a failing regression fixture for the over-selected path combination.
3. Implement and verify change-impact selection and a stable required gate.
4. Use a CI-policy PR to test the conservative full path.
5. Exercise a docs-only canary PR to prove the expensive jobs are skipped,
   without weakening the expected required statuses.
6. Record measured before/after runner job-minutes; merge only once all
   required checks and independent review are complete.

Do not consider a green CI-policy PR sufficient proof of a docs-only path:
a CI-policy PR must select the broad safety path by design.
