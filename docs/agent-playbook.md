# Agent Playbook

## Source Of Truth
- `README.md` for repository scope.
- `CONTRIBUTING.md` for contribution flow and commit conventions.
- `SECURITY.md` and `SUPPORT.md` for escalation paths.
- `profile/README.md` for org profile content.

## Repository Map
- `profile/` contains the public organization profile.
- Root Markdown files define shared contributor guidance used across repositories.

## Change Workflow
1. Read the existing policy files before editing wording.
2. Keep terminology consistent across all community files.
3. If you add a new policy, update the most relevant existing document instead of creating redundant guidance.
4. Check for broken links and obvious formatting regressions before committing.
5. Apply the unified PR process from root CONTRIBUTING.md without introducing tool-specific mandatory Oracle/Copilot review routes; use actual repo CI commands and keep security/release safeguards.

## Validation
- Review Markdown files with `rg -n '^#|^##|^###' *.md profile/README.md`.
- If you change issue, PR, or branch guidance, confirm it does not conflict with active repository practices.
