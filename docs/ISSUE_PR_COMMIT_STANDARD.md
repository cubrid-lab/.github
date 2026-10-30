# Issue, pull request, and commit writing standard

This is the shared baseline for **cubrid-lab**. Repository-specific technical requirements and existing PR/commit CI checks take precedence when they are stricter or different (for example, the CUBRID engine's ticket-number PR convention). Do not overwrite local build, security, or release rules.

## 1. Issue: identify the problem or goal

Use a **type-only** prefix in plain English; do not require or guess a module/scope when the issue is opened:

```text
feat: schedule HA database members on separate nodes by default
bug: prevent duplicate reconciliations after leader changes
docs: explain the supported upgrade procedure
test: verify recovery after node power loss
chore: refresh dependency support matrix
ci: verify release workflows before publishing
```

- **Every issue title needs a type prefix.** Use `feat:` for a new capability, `bug:` for observed defects, and `docs:`, `test:`, `chore:`, or `ci:` as appropriate. Keep the prefix lowercase, followed by one space; do not drop it when making a title more human-readable.
- **Issue `bug:` intentionally differs from Conventional Commits `fix:`**: bug describes an unresolved problem, whereas fix describes a completed change.
- The goal or observed behavior must be specific, human-readable, searchable and understandable without internal project knowledge. Prefer "what should happen" or "what fails" over implementation guesses.
- Do not require `type(scope):` in an issue. Do not add private review codes, milestone/test IDs, agent bookkeeping, personal notes, named maintainer comments or ambiguous abbreviations solely to the title/body.
- For a reported bug, distinguish observed facts, reproduction steps, expected/actual outcomes and the environment. If it is not reproduced, explicitly state the limitation.
- For a feature, explain the motivation, expected behavior and **observable acceptance criteria**, including necessary constraints. Tests should demonstrate the behavior they can actually exercise; simulated tests are not evidence of real-cluster scheduling, availability or persistence.
- Avoid prescribing detailed implementation or listing individual files until it is needed for a validated design; keep alternatives and unresolved decisions clear. Keep a small documentation/task issue short rather than forcing a lengthy template.
- Apply the same convention across all `cubrid-lab` repositories, including issue forms, repository-specific agent instructions, and existing issues. Audit open issues regularly and correct missing or inaccurate type prefixes and opaque titles. During an explicitly requested retrospective cleanup, review closed issues as well. Preserve issue meaning, technical evidence, internal identifiers in the body, links, labels, ownership and state; do not classify issues solely by a PR or commit title.
- Keep older or already-clear issue prose intact unless an actual readability defect is identified. Bulk edits must not replace detailed evidence with generic summaries, erase release or security requirements, or alter a historical conclusion. If an issue's type is genuinely ambiguous, review its body before changing its title.

## 2. Triage: decide what work is valid

- New issues begin with the existing `status: needs triage` label (or the canonical local equivalent). API/agent-created issues must attach it at creation when events cannot retrigger the labeling workflow.
- Review reproducibility/validity, duplication, correct repository, type, clear scope, dependencies and acceptance criteria.
- Set exactly one `priority: critical/high/medium/low` and one `size: XS/S/M/L/XL`, using the repository's actual label spelling. Compare priorities against **all open issues in that repository**, not only the new item.
- Confirm the labels persisted and the review is complete before removing needs-triage. Never infer priority, size, or acceptance from the title prefix alone.
- Retain the issue's original goal during refinement; if implementation reveals additional work, record separate follow-ups instead of silently expanding scope.

## 3. Pull request: describe the implemented change

- Use **Conventional Commits** for PR titles where supported, e.g. `feat(placement): enforce node anti-affinity for HA members`, `fix(controller): avoid duplicate reconciliations`, `docs: clarify installation prerequisites`.
- A PR title describes what was actually changed, not only the desired result from the issue. A meaningful scope is allowed but not required unless the repository-specific validator demands it. Prefer a meaningful behavior or change over an opaque scenario, test-lane, or project-internal code; place such identifiers in the body when useful.
- Keep PR descriptions readable for someone outside the immediate implementation: lead with the motivation and behavior changed, then summarize important changes, validation actually performed, known limits/follow-ups, and related issues. Put raw logs and long test-by-test evidence in collapsible details or linked artifacts when needed; do not bury the result in template repetition or agent-generated narration. Avoid boilerplate AI author credits or automated-review marketing in permanent descriptions.
- Include motivation, changed behavior, related issue (`Closes #N` or `Refs #N` as applicable), test results actually observed, skipped validation, backwards compatibility and notable risks. Do not treat automated or AI-assisted review as a substitute for verified tests.
- PR CI checks the PR title format and repository-specific quality gates. It must not automatically decide issue validity, impact, effort, or acceptance-criteria completion.
- Preserve existing local PR-title validators and branch protections; do not change them merely to standardize issue titles.

## 4. Commit: record a completed change

Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, etc.), with optional meaningful scope. In squash-merge repositories, ensure the PR title produces a suitable final commit subject.

## 5. Human/agent parity

Apply the same policy to humans, Codex, Claude Code, OpenCode and other agents. Keep instructions tool-neutral and grounded in repository evidence. Do not copy author-specific comments, reviewer names or AI-workflow narration into permanent issue prose unless attribution itself is materially necessary.

## 6. Explanations in code, tests, reviews and agent-written text

This is the canonical rule for explanatory prose written by people or agents: source-code comments, test names and test comments, examples, PR descriptions, review comments and replies, status comments and published explanations.

- Explain **what happens, why it matters, and the invariant or constraint involved** in ordinary English. A reader should understand the comment or reply without opening a past PR, an issue thread, a scenario table or an agent's private notes.
- An unexplained issue number, scenario or test-lane code (`S06`), `see above`, `as discussed`, or agent-only shorthand must not stand in for the explanation. Put the explanation first; add the identifier afterwards for traceability.
- Issue numbers and identifiers are **not defects** by themselves. Keep machine-readable identifiers unchanged where they are part of code, test discovery, fixture names, artifact paths, error codes, structured data or exact evidence references.
- Do not add comments that only restate self-explanatory code, and do not delete useful history. Revise existing text only where a real reader would be confused.

Example:

```go
// Bad: the reason lives in another scenario and an issue thread.
// A heartbeat status that was not answered observed nothing, as in S12 (#607).

// Good: the behavior and the decision are explained; the IDs stay for traceability.
// If the heartbeat command cannot reach a member or return its role, the
// post-restart HA state cannot be observed. Report it as blocked rather than
// failed unless another invariant violation was already seen (S06, #607).
```

A review reply such as `fixed per S12` is likewise incomplete; `The retry now stops after the cluster read succeeds, so a slow member no longer fails the whole check (S12)` can be checked by any maintainer.

### Adoption by each repository

- Changes to this file or to this repository's `AGENTS.md` are **not inherited automatically** by other repositories' `AGENTS.md` files, and no coding agent is guaranteed to read or follow them.
- Each repository adopts the rule by linking this section from its own agent instructions (`AGENTS.md`, or the contributor guide it points to). Do not copy the whole policy; a short pointer plus any repository-specific notes is enough.
- Repository-specific safety, build, release and content rules keep precedence. When maintaining local guidance, check it for conflicts with this section and resolve them in a normal PR.
- This is a writing convention, not a CI check, bot, merge gate or required reviewer.

### Review checklist

Run through this by hand when writing or reviewing a new comment, test name, PR description or review reply:

1. Does it say what happens or what was changed, in plain words?
2. Does it say why: the reason, invariant or constraint?
3. Can a maintainer new to the change understand it without opening another issue, PR, scenario table or agent log?
4. Is every internal code or issue number explained in the same sentence, or kept only for traceability?
5. Are machine-readable identifiers (test names used for discovery, fixtures, error codes, paths) left intact?
6. Is the comment needed at all, or does the code already say it?
