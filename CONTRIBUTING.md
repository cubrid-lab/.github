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

Ultraworked with [Sisyphus](https://github.com/code-yeongyu/oh-my-opencode)
Co-authored-by: Your Name <your.email@example.com>
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

1. Ensure all tests pass locally
2. Ensure code coverage meets repository threshold (typically 95%+)
3. Ensure linting and formatting pass
4. Request review from maintainers
5. Address feedback and push updates
6. Rebase and merge once approved

## License

All contributions are licensed under the **MIT License**. By contributing, you agree to license your work under these terms.

## Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing. We are committed to providing a respectful and inclusive community for all participants.

---

**Questions?**
- 💬 Post in [GitHub Discussions](https://github.com/orgs/cubrid-lab/discussions)
- 📧 Contact maintainers via the issue tracker

Thank you for contributing to CUBRID Labs!
