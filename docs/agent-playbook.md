# Agent Playbook

## Source Of Truth
- `README.md` for repository scope.
- `CONTRIBUTING.md` for contribution flow and commit conventions.
- `SECURITY.md` and `SUPPORT.md` for escalation paths.
- `profile/README.md` for org profile content.

## Repository Map
- `profile/` contains the public organization profile.
- Root community files provide GitHub-supported fallback templates where applicable; this repository's agent and engineering documents are not inherited by other repositories.

## Change Workflow
1. Read this repository's active community files and distinguish them from historical engineering policy notes.
2. Keep terminology consistent across all community files.
3. Keep changes scoped to this repository; do not add central policies that purport to govern product repositories.
4. Check for broken links and obvious formatting regressions before committing.
5. For this repository, follow root CONTRIBUTING.md and its own CI/security checks. Other repositories retain their own review, CI and release safeguards.

## Validation
- Review Markdown files with `rg -n '^#|^##|^###' *.md profile/README.md`.
- If you change issue, PR, or branch guidance, confirm it does not conflict with active repository practices.
