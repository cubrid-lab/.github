# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in any CUBRID Labs project, **please do not open a public issue**. Instead, follow one of these secure reporting methods:

### Option 1: GitHub Security Advisories (Preferred)

Use the **Private Vulnerability Reporting** feature on each repository:

1. Go to the repository's **Security** tab
2. Click **Report a vulnerability**
3. Fill out the form with details about the vulnerability
4. Submit — this creates a private advisory visible only to maintainers

### Option 2: Email

If you prefer email, contact the maintainers directly with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

Check the individual repository's `SECURITY.md` file for specific contact information.

## Vulnerability Disclosure Timeline

- **Initial Report**: Acknowledgment within 24–48 hours
- **Assessment**: Severity determination and impact analysis (1–7 days)
- **Fix Development**: Patch development and testing (depends on complexity)
- **Coordinate Release**: Public disclosure coordinated with fix release
- **Public Disclosure**: Security advisory published after patch is available

## Supported Versions

Security updates are provided for:
- **Latest major version**: All patch versions
- **Previous major version**: Critical fixes only

Check individual repository documentation for specific version support policies.

## Security Best Practices

When using CUBRID Labs projects:

1. **Keep dependencies updated** — Regularly update the driver/ORM to the latest version
2. **Use TLS for connections** — Always encrypt database connections in production
3. **Validate input** — Avoid SQL injection by using parameterized queries (not string interpolation)
4. **Restrict permissions** — Use least-privilege database accounts
5. **Monitor logs** — Track authentication failures and unusual queries

## Thank You

We appreciate responsible security disclosures and will credit researchers in security advisories (unless they prefer anonymity).

---

**Questions about security?** Post in [GitHub Discussions](https://github.com/orgs/cubrid-lab/discussions/categories/security) or email the maintainers.
