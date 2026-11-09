# Contributing to CUBRID Labs

Thank you for contributing to CUBRID Lab. This repository maintains the organization's GitHub community defaults and public profile. GitHub can use supported community files as fallbacks where a project has no local version, but **engineering policies and agent instructions here are not inherited**. Always use the target project's own contribution, test and release requirements.

## Issue, PR, and commit titles

For issues and PRs **in this repository**, use a descriptive type-only issue title (`docs:`, `bug:`, `ci:`, etc.) and a clear PR title matching the actual change. Include evidence, local validation and measurable acceptance criteria. Other repositories own their issue and PR formats and the checks that enforce them. The prior [cross-repository writing standard](docs/ISSUE_PR_COMMIT_STANDARD.md) is historical, not a requirement.

## How to Contribute

### Reporting Issues

- **Bugs**: Open an issue in the relevant repository with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs. actual behavior
  - Environment details (Python/Node.js/Go version, OS, dependency versions)

- **Feature Requests**: Open a discussion or issue describing:
  - The problem you're solving
  - Proposed solution
  - Alternative approaches considered

### Pull Requests

1. **Fork** the repository and create a focused branch from its current default branch
2. **Develop** your changes with clear, focused commits
3. **Test** your changes (see repository-specific docs)
4. **Document** your changes with comments and docstrings
5. **Submit** a pull request with:
   - Clear title and description
   - Reference to related issues
   - Explanation of changes and rationale

### Discussions

Use [GitHub Discussions](https://github.com/orgs/cubrid-lab/discussions) for:
- Questions about usage
- Design proposals
- Architecture discussions
- Community ideas

For background on connector styles, the [language-native connector notes](docs/LANGUAGE_NATIVE_CONNECTORS.md) are optional reading, not a cross-repository design requirement. Design and release decisions belong to the owning project.

## Development Setup and code style

Every repository controls its language-specific tools, runtime compatibility,
tests, documentation and release process. Before changing code, consult
the owning repository's `CONTRIBUTING.md`, manifests, build scripts and
GitHub Actions workflows. Their actual commands override examples given here.

The [language-specific repository index](docs/LANGUAGE_DEVELOPMENT_POLICY.md) may help locate project instructions, but it does not override any repository's own toolchain or release procedure.

Do not assume Python always has the same Ruff or Mypy version, every
TypeScript project uses ESLint/Prettier rather than Biome, or every
repository includes a `make lint` or `npm run format` script. Use
the tools, version pins and non-mutating CI checks that the repository
**actually** defines. This common guidance does not mandate a new
formatter, compiler, test framework or CI gate.

The former [change-impact CI policy](docs/CI_CHANGE_IMPACT_POLICY.md) is historical. Each repository chooses and verifies its own risk-appropriate CI selection.

## Commit Convention

For commits to this `.github` repository, use:

```
<type>: <description>

<optional body>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `chore`: Build, CI, dependency updates, or non-functional changes
- `ci`: CI/CD workflow changes
- `style`: Code style (formatting, linting)
- `test`: Test additions or improvements
- `refactor`: Code refactoring without feature changes

**Examples:**

```
feat: add CUBRID type mapping for CLOB and BLOB

Implements full support for CUBRID collection types (SET, MULTISET, SEQUENCE).
Adds comprehensive test coverage and documentation.

fix: handle NULL values in ON DUPLICATE KEY UPDATE

Resolves issue where NULL values in conflict resolution caused type errors.
```

## Issue intake and ownership

File issues in the repository that owns the change, not in a central development
tracker. New reports start as `status: needs triage`: maintainers confirm the
problem, duplicates, issue type, scope and relative priority against the local
open backlog. The exact labels are `priority: critical/high/medium/low` and
`size: XS/S/M/L/XL`; only after checking the saved labels and review outcome
may they remove the triage status. Issue priority is not PR approval or job
readiness.

Outside contributors can work on unclaimed issues without prior assignment.
Maintainer-operated autonomous agents must have authorization and a confirmed
assignee before implementing internal tasks; check existing PRs before starting.
Issue templates/automation and exceptions belong to the individual repository.

## Pull Request Process

The process below applies to contributions **to this repository**, regardless of implementation tool (human-authored or AI-assisted). Other repositories have their own PR processes.
No contributor is required to install or obtain a review from a particular AI tool.

1. **Create a focused PR.** Describe why the change is needed, what it changes,
   its tests, and any affected documentation. Contributors may work on unclaimed
   issues without prior assignment, subject to the repository's coordination rules.
2. **Validate through GitHub CI.** Required GitHub Actions checks are the
   authoritative test result. They must pass on the final relevant head before
   merge, including repository-appropriate lint, format, unit, integration/live,
   security and documentation checks. For forks awaiting Actions approval, a
   maintainer reviews the proposed changes before allowing workflows to run.
   Local tests are helpful and should be reported honestly but are not an
   additional mandatory gate.
3. **Review the changes.** Reviewers assess correctness, tests, risk, security,
   maintainability and scope. AI-assisted code review (Oracle, Copilot,
   `agent-review`, etc.) is optional and advisory only. Bot summaries or green
   CI never imply a maintainer approval.
4. **Address findings.** Correct verified defects, record accepted exceptions or
   follow-ups, and rerun required checks after updates. Do not merge with
   unresolved critical/security defects or failing required checks.
5. **Maintainer merge decision.** The responsible maintainer confirms the final
   head, required checks, review outcome and any project-specific release
   requirements. Security-sensitive, high-impact workflow/permission and
   publishing changes require an independent maintainer's approval when
   applicable. Keep existing branch protections; adjust them only via an
   intentional, separately reviewed repository-specific change.

For CI changes in this repository, verify its own required status checks and safe behavior. CI changes in another repository must be assessed against that repository's actual workflows, supported tests and permissions.

Each repository documents its own test commands and risk-sensitive paths. The
**review criteria** stay the same across repositories, even when CI runner
infrastructure differs. Use squash merge where repository rulesets prescribe it.

Tool attribution is optional and should be factual; add a coauthor trailer only
for a real contributor and only when permitted by the target project. Do not
insert named agent credits or boilerplate trailers in every commit.

## License

Contributions follow the **license of the target repository** (for example, the CUBRID engine and individual drivers may use different licenses). Check that repository's `LICENSE` and contribution requirements before submitting; do not assume every CUBRID Lab project uses MIT.

## Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. We are committed to providing a respectful and inclusive community for all participants.

---

**Questions?**
- 💬 Post in [GitHub Discussions](https://github.com/orgs/cubrid-lab/discussions)
- 📧 Contact maintainers via the issue tracker

Thank you for contributing to CUBRID Labs!

## Finding Work (labels)

| Label | Meaning |
|---|---|
| `good first issue` | Small, scoped, acceptance criteria written — maintainers will mentor |
| `help wanted` | Maintainers welcome an external PR and will answer questions |
| `size: XS`–`XL` | Expected change size |
| `area: ...` | Repo-specific domain (e.g. `area: async`) |
| `bug` / `enhancement` / `documentation` | Work type (auto-applied by issue templates) |

The full org label scheme lives in [`.github/labels.yml`](.github/labels.yml).
