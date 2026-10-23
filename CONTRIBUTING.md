# Contributing to CUBRID Labs

Thank you for your interest in contributing to CUBRID Labs! We welcome contributions from the community in the form of bug reports, feature requests, code contributions, documentation, and more.

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

1. **Fork** the repository and create a feature branch from `main`
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

## Development Setup

Each repository provides detailed setup instructions:

- **Python projects**: See `DEVELOPMENT.md` (usually includes `make install`, `make test`, `make lint`)
- **TypeScript projects**: See `README.md` (usually includes `npm install`, `npm test`, `npm run lint`)
- **Go projects**: See `README.md` (usually includes `go test`, `go fmt`)

Typically, all projects include:
- Automated linting and formatting
- Pre-commit hooks (where applicable)
- CI/CD validation on pull requests

## Code Style

We follow language-specific conventions:

### Python

- Formatter: **Ruff** (target: 100-character line length)
- Style: PEP 8 with type hints (PEP 561)
- Tool: `make format` (or `ruff format` + `ruff check --fix`)

### TypeScript

- Formatter: **ESLint** + **Prettier**
- Style: ES6+, strict typing, null coalescing
- Tool: `npm run lint` / `npm run format`

### Go

- Formatter: **gofmt**
- Style: idiomatic Go, interfaces over concrete types
- Tool: `gofmt -w` or `make fmt`

## Commit Convention

Follow this format for all commits:

```
<type>: <description>

<optional body>

Co-authored-by: Contributor Name <contributor@example.com>
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

## Pull Request Process

The same process applies to all contributions regardless of implementation tool
(human-authored, OpenCode, Codex, Claude Code, Copilot, ChatGPT, or other agents).
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

Each repository documents its own test commands and risk-sensitive paths. The
**review criteria** stay the same across repositories, even when CI runner
infrastructure differs. Use squash merge where repository rulesets prescribe it.

Tool attribution is optional and should be factual; do not add generic,
tool-specific commit footers to every contribution.

## License

All contributions are licensed under the **MIT License**. By contributing, you agree to license your work under these terms.

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
