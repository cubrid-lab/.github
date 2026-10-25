# AGENTS.md

## Purpose
This repository holds organization-wide community health files for `cubrid-lab`.

## Read First
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `SUPPORT.md`
- `docs/agent-playbook.md`

## Working Rules
- Treat this repo as policy and template infrastructure, not product code.
- Keep contributor-facing guidance consistent across files.
- When behavior or policy changes, update every affected document in the same change.
- Prefer small edits that preserve existing wording unless a policy change is intentional.

## Development Workflow (cubrid-lab org standard)

Every contribution follows the same review and merge process, **regardless of
whether code was written by a person, OpenCode, Codex, Claude Code, ChatGPT,
Copilot, or another agent**. The canonical policy is in
[CONTRIBUTING.md](CONTRIBUTING.md#pull-request-process).

1. **Scope and implementation** — Keep an issue/PR focused. Include tests and
   affected documentation in the PR; explain when documentation does not change.
2. **GitHub CI** — Treat the repository's required GitHub Actions checks as the
   authoritative verification record. Run applicable formatting, lint, tests,
   documentation, security and integration/live checks. Local checks are
   encouraged but do not replace required CI and are not a separate gate.
3. **Code review** — Assess behavior, tests, scope, maintainability and
   security. Optional reviews from Oracle, Copilot, `agent-review` and other AI
   tools are advisory evidence, not required by implementation tool and never a
   substitute for maintainer judgment.
4. **Final verification and merge** — Recheck the final PR head and required CI;
   resolve or document actionable findings. The responsible maintainer decides
   whether to merge. An independent maintainer approval is required for
   security-sensitive, release/publishing, or high-impact CI/permission changes,
   where available; never silently weaken existing repository protections.

Avoid mandatory Oracle pre/post reviews, Copilot reviews, fixed AI review-round
budgets or separate approval routes based on the tool used. Existing branch
rulesets, security controls, release safeguards and repository-specific
test commands remain authoritative; changes to those controls need their own
reviewed PR.

## Issue intake and autonomous agent work

The rules here describe a **shared decision process**, not a mandatory
cross-repository tool or a new CI gate. Each repository's own `AGENTS.md`,
`CONTRIBUTING.md`, tests, code ownership and safety/release rules determine
the actual implementation commands and any additional approvals.

- **Before filing:** verify the problem against current code, open/recently
  closed issues and overlapping PRs. File a focused, testable issue only in
  the repository whose code or documentation needs to change.
- **Triage:** newly filed issues enter `status: needs triage`. Review validity,
  duplicates, type, scope, readiness and all open issues **in that repository**.
  Confirm one `priority: critical/high/medium/low` and one existing
  `size: XS/S/M/L/XL`; priority measures urgency, size estimates effort.
  Read back saved GitHub labels before clearing the triage status. Do not
  automate severity guesses or clear triage based on labels alone.
- **Ownership:** outside human contributors can report or improve unclaimed
  work without preapproval or mandatory self-assignment. Maintainer-operated
  autonomous agents need explicit authorization and a verified GitHub assignee
  before implementing internally assigned work; coordinate with the owner
  of any overlapping PR.
- **Implementation:** use the smallest change meeting checked acceptance
  criteria. Do not introduce speculative abstractions, mandatory AI review
  stages, extra CI gates or generic infrastructure for a documentation fix.
- **Completion:** report real checks run, skipped checks and residual risk.
  Required final-head CI and maintainer review decide merge readiness; after
  merge, reconcile only genuinely superseded issues and PRs.

## Validation
- Manually review Markdown rendering and link targets.
- If examples or command snippets change, verify they still match current org conventions.

## Historical project context — Performance Loop System

The following dated plan and team agreements record an earlier initiative.
They are **not organization-wide contribution prerequisites, active issue
triage gates or restrictions on independent repository work**. Preserve the
history, but use current repository-specific issues and requirements for work.

> **Board**: [CUBRID Ecosystem Roadmap](https://github.com/orgs/cubrid-lab/projects/2) (maintainers only)

### What This Is

A continuous **Performance Loop** across the CUBRID ecosystem:
benchmark → profile → optimize driver/ORM → re-benchmark → CI-verified regression prevention.

### Core Repos

Current release versions: live badges in [`profile/README.md`](profile/README.md).

| Repo | Role | Current State |
|------|------|---------------|
| `cubrid-benchmark` | Benchmark suite (Python/TS/Go × CUBRID/MySQL) | Tier 0+1+Extended, CI, GitHub Pages — **most mature** |
| `pycubrid` | Python driver (PEP 249) | stable 1.x on PyPI — **async TLS + STARTTLS hardening, transport contract lock, 1.x compat-check CI gate; 2 perf cycles complete, 19% fetch improvement** |
| `sqlalchemy-cubrid` | SQLAlchemy 2.0–2.1 dialect | stable 1.x on PyPI — **SQLAlchemy 2.0–2.1 compat shims, async integration stability; query compilation optimized** |
| `cubrid-mcp-server` | MCP server (LLM ↔ CUBRID) | 0.x beta on PyPI — **11 read-only tools plus opt-in `execute_write`, read-only whitelist + opt-in write mode, multi-connection, audit log, docs site live** |
| `cubrid-cookbook` | Runnable examples across all languages | Python: **68 examples, 45 CI golden-verified on CUBRID 11.2 + 11.4**, one-command dashboard template; other languages planned |

## Translation Policy (cubrid-lab org)

English is canonical. 한국어 (`docs/README.ko.md`) is **required-to-sync** — a PR
changing `README.md` without it fails the `translation-sync` check (escape hatch:
`translations-deferred` label). Other languages (de/hi/ru/zh) are community
translations: drift emits a warning only; maintainers' AI agent opens resync PRs.
This hard gate is time-boxed for the 2026 contest finals and should be relaxed to
advisory afterwards (see the reminder issue).

## Roadmap Update Policy

The ecosystem roadmap (`ROADMAP.md`) is a living document. It MUST be updated:
- **On every release** — version bump + status change in the same PR as the release
- **On every significant feature** — new items in the "Now" section of the feature PR
- **On milestone completion** — move from "Next" to "Now" to completed

If a PR changes public behavior, adds features, or bumps versions, the PR body must
include `Roadmap: updated` or `Roadmap: not needed - <reason>`.
This is enforced by code review, not CI (roadmap changes require human judgment).

## Operations Manual

Releases, docs sites, CI gates, secrets, and the gotchas behind them:
[docs/OPERATIONS.md](docs/OPERATIONS.md). Update it in the same PR that
changes any release/docs/CI convention.

## Issue intake and maintainer triage

For issues filed **in this repository**, begin with `status: needs triage`;
`issues: opened` automation marks external submissions. Issue forms also
carry the status, and agents creating issues through `GITHUB_TOKEN` must
explicitly set it on creation because those events may not retrigger Actions.

1. Verify the problem, evidence or unknowns, duplicates (including open PRs),
   scope, issue type, acceptance and actual dependencies; close invalid or
   duplicate requests with a reason.
2. Compare **all open issues in this repository** before assigning relative
   urgency, taking account of current priorities, security, blocked work and
   impact. Explain when another priority must change.
3. Assign one `priority: critical/high/medium/low` and one existing
   `size: XS/S/M/L/XL`, preserving unrelated labels and assignees. Split
   overlarge implementation tasks when independently verifiable.
4. Re-fetch actual issue labels, confirm validity, type, priority and size,
   then remove `status: needs triage` manually. Never let a workflow choose
   priority, close duplicates or clear triage based only on label presence.

These issue-management rules do not change the organization label catalog
or authorize cross-repository master trackers. Every other repository owns
its issue decisions and can adopt the same workflow independently.

## Label Rules (cubrid-lab org)

Source of truth: [`.github/labels.yml`](.github/labels.yml) — sync with
`python scripts/sync_labels.py`, drift reported weekly by `label-audit`.
Naming: lowercase, spaced-colon prefixes (`priority: high`, `size: S`,
`area: packaging`). Escape-hatch labels (`docs-not-needed`,
`translations-deferred`) share one color. `good first issue` and
`help wanted` are maintainer promises (scoping + mentoring), never
auto-applied. Domain labels are repo-optional `area: ...` only.

### Supporting Repos

`cubrid-client` (TS), `cubrid-go`, `cubrid-rs`, `drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`

### Execution Phases

| Phase | Period | Focus |
|-------|--------|-------|
| R0: Baseline Reset | Week 1-2 | Scope reset, baseline recording, plan rewrite |
| R1: Measurement | Week 3-5 | Tier 2 ORM benchmarks, reproducibility policy |
| R2: Python Optimization | Week 6-10 | pycubrid profiling, serialization + cursor fetch optimization |
| R3: ORM Validation | Week 11-14 | sqlalchemy-cubrid optimization, 2nd pycubrid cycle |
| R4: Stability | Week 15-18 | cubrid-client resilience (nice-to-have) |
| R5: CI & Regression | Week 19-22 | Compare script, cookbook standardization |
| R6: Finalization | Week 23-32 | Evidence pack, demo, documentation |

### Hero Metric

**Python driver MySQL 대비 성능 갭 감소** — before/after 수치가 핵심 스토리.

### Decision Gate (Week 8)

pycubrid 최적화 결과 +10% 이상이면 계속, 미만이면 Go/TS 성과 중심으로 내러티브 피벗.

### Narrative

"Build Once, Improve Continuously" — 매일 밤 자동 벤치마크, PR마다 회귀 감지, 재현 가능한 one-command 데모.

### Must-Have Deliverables

1. pycubrid before/after 성능 수치
2. Tier 2 ORM 벤치마크
3. Performance Loop 2회 이상 완주 증명
4. one-command 재현 데모 (`docker compose up && make demo`)
5. 증거팩 (차트, 보고서)

## Historical team coordination (2-Person Team)

The notes below describe a past, internally coordinated team process. They do
not require outside contributors to obtain an assignee, prohibit legitimate
collaboration, impose a fixed branch prefix, or block unrelated upstream and
downstream contributions. Active ownership is established by the target
repository's actual GitHub issue, PRs and maintainer guidance.

### Rules

1. **Issue assignment is mandatory before starting work.** GitHub issue에 본인을 assign한 뒤 작업 시작. assign 안 된 이슈는 누구도 작업 중이 아님.
2. **한 이슈에 한 사람.** 같은 이슈에 두 사람이 동시에 작업하지 않는다.
3. **같은 파일 수정 금지.** 서로 다른 이슈더라도 같은 파일을 동시에 수정하면 충돌. 의심되면 먼저 PR 올린 사람이 우선.
4. **Branch naming**: `{username}/{issue-number}-short-description` (예: `jay/19-profiling`)
5. **PR 검토 및 병합.** 필수 GitHub CI 결과와 변경 영향을 확인한 후 책임 Maintainer가 병합을 결정한다. 보안·배포 등 고위험 변경은 독립적인 Maintainer 검토를 거친다.
6. **Phase 순서 존중.** Backlog에 있는 이슈는 해당 Phase의 선행 이슈가 Done이 될 때까지 착수하지 않는다.

### Parallel Work Guidelines

동시 작업 가능한 조합 (충돌 없음):
- Person A: `cubrid-benchmark` repo / Person B: `pycubrid` repo
- Person A: R1 measurement 이슈 / Person B: R2 profiling 준비 (단, R2 본격 최적화는 R1 완료 후)
- Person A: 벤치마크 인프라 (#6, #9) / Person B: profiling 인프라 (#14, #15)

동시 작업 **금지** 조합:
- 같은 repo의 같은 모듈 (예: 두 사람이 동시에 pycubrid/protocol.py 수정)
- upstream/downstream 동시 수정 (예: pycubrid API 변경 + sqlalchemy-cubrid에서 해당 API 사용)

### Daily Sync

- 작업 시작 전 GitHub Project Board 확인 → In Progress 상태 업데이트
- 작업 완료 시 즉시 PR 생성 + Done 이동
