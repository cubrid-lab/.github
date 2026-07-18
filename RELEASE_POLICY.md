# Release Policy

This document defines the standard release process for all cubrid-lab product repositories. Apply it consistently across `pycubrid`, `sqlalchemy-cubrid`, `cubrid-cookbook-python`, and future repos.

## Pre-release checklist

For every release (patch, minor, major), complete the following:

### Code & version
- [ ] All planned issues for this milestone are closed or rescheduled
- [ ] `pytest` (offline suite) passes with coverage ≥ threshold (95% for drivers)
- [ ] Integration tests pass against all supported CUBRID versions
- [ ] Version bumped in `pyproject.toml`
- [ ] Version bumped in `<package>/__init__.py` (`__version__`) where applicable
- [ ] CHANGELOG entry added (Keep a Changelog format)

### Documentation
- [ ] README badges (version, supported matrices) reflect new release
- [ ] README Compatibility / Support Status section matches actual tested matrix
- [ ] `SUPPORT_MATRIX.md` (if present) matches badges
- [ ] `ROADMAP.md` updated: completed items moved to "Completed", next milestone revised
- [ ] All `docs/` files reviewed for stale references
- [ ] Link checker (see [`docs/LINK_CHECK.md`](LINK_CHECK.md)) is green on the release branch

### About metadata (Settings → About)

> **This step is commonly forgotten.** About is the first thing a visitor sees in the GitHub UI — above the README. Treat it as part of the release.

- [ ] **Description** — review and update:
  - version range (e.g., "SQLAlchemy 2.0–2.2 dialect")
  - framework/library name(s)
  - key feature highlights
- [ ] **Homepage / Website** — points to the current docs URL (typically `https://cubrid-lab.github.io/<repo>/`)
- [ ] **Topics** — accurate, no stale tags from prior repo scope (e.g., no `nodejs` on a Python-only repo)

Programmatic update:

```bash
gh repo edit cubrid-lab/<repo> \
  --description "<new description>" \
  --homepage "<docs URL>"

# Topics are add/remove:
gh repo edit cubrid-lab/<repo> --remove-topic <stale-tag>
gh repo edit cubrid-lab/<repo> --add-topic <new-tag>
```

### Release mechanics
- [ ] Tag created: `git tag vX.Y.Z`
- [ ] Tag pushed: `git push origin main --tags`
- [ ] GitHub Release created via `gh release create vX.Y.Z --title "..." --notes "..."` (or generated from CHANGELOG)
- [ ] PyPI publish (for Python packages) — verify Trusted Publisher flow triggered
- [ ] Release notes proofread

### Post-release
- [ ] Announcement (if applicable)
- [ ] Milestone closed on GitHub
- [ ] Next milestone created with target date

## See also

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- Org-wide [link checker](docs/LINK_CHECK.md) — catches broken links before users do
