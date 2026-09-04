# CUBRID Lab

<div align="center">

[![GitHub Organization](https://img.shields.io/badge/GitHub-cubrid--lab-181717?logo=github)](https://github.com/cubrid-lab)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Modern database tooling for CUBRID — Python, TypeScript, Go, Rust**

*A comprehensive ecosystem of drivers, ORMs, and tools for building applications with CUBRID.*

</div>

---

> **Independence notice**  
> CUBRID Lab is an independent, community-driven open-source initiative building modern developer tooling for the CUBRID database. It is maintained independently and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; use of the name here is solely to identify compatibility with the CUBRID database.

---

## 한국어 소개

CUBRID Lab은 CUBRID 데이터베이스를 위한 현대적이고 생산성 높은 도구들을 개발하고 유지보수하는 조직입니다. Python, TypeScript, Go, Rust 등 다양한 언어로 드라이버, ORM, 예제 코드를 제공하여 개발자들이 CUBRID를 쉽고 효율적으로 사용할 수 있도록 합니다.

> **독립성 안내**  
> CUBRID Lab은 CUBRID 데이터베이스를 위한 현대적인 개발자 도구를 만드는 독립적인 커뮤니티 주도 오픈소스 이니셔티브입니다. CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴, 후원 또는 보증 관계가 없으며, 공식 CUBRID 프로젝트가 아닙니다. CUBRID 명칭은 CUBRID 데이터베이스와의 호환성을 설명하기 위해 사용됩니다.

---

## Projects

### Python

| Repository | Role | Version | Description | Status |
|---|---|---|---|---|
| **[pycubrid](https://github.com/cubrid-lab/pycubrid)** | Driver | v1.7.0 ![stable](https://img.shields.io/badge/-stable-brightgreen) | Pure Python DB-API 2.0 (PEP 249) driver — sync + native asyncio, TLS/SSL with STARTTLS | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/pycubrid/ci.yml?label=tests)](https://github.com/cubrid-lab/pycubrid/actions) [![PyPI](https://img.shields.io/pypi/v/pycubrid)](https://pypi.org/project/pycubrid) |
| **[sqlalchemy-cubrid](https://github.com/cubrid-lab/sqlalchemy-cubrid)** | ORM | v1.7.0 ![stable](https://img.shields.io/badge/-stable-brightgreen) | SQLAlchemy 2.0–2.2 dialect + Alembic | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/sqlalchemy-cubrid/ci.yml?label=tests)](https://github.com/cubrid-lab/sqlalchemy-cubrid/actions) [![PyPI](https://img.shields.io/pypi/v/sqlalchemy-cubrid)](https://pypi.org/project/sqlalchemy-cubrid) |
| **[cubrid-mcp-server](https://github.com/cubrid-lab/cubrid-mcp-server)** | AI/LLM | v0.3.1 ![stable](https://img.shields.io/badge/-stable-brightgreen) | Model Context Protocol server for CUBRID — enables LLMs to inspect schemas and run read-only queries | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/cubrid-mcp-server/ci.yml?label=tests)](https://github.com/cubrid-lab/cubrid-mcp-server/actions) [![PyPI](https://img.shields.io/pypi/v/cubrid-mcp-server)](https://pypi.org/project/cubrid-mcp-server) |

### TypeScript / Node.js

| Repository | Role | Version | Description | Status |
|---|---|---|---|---|
| **[cubrid-client](https://github.com/cubrid-lab/cubrid-client)** | Driver | v1.1.0 ![stable](https://img.shields.io/badge/-stable-brightgreen) | TypeScript-first async client | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/cubrid-client/ci.yml?label=tests)](https://github.com/cubrid-lab/cubrid-client/actions) [![npm](https://img.shields.io/npm/v/cubrid-client)](https://www.npmjs.com/package/cubrid-client) |
| **[drizzle-cubrid](https://github.com/cubrid-lab/drizzle-cubrid)** | ORM | v0.2.1 ![beta](https://img.shields.io/badge/-beta-yellow) | Drizzle ORM dialect with type-safe schema | [![npm](https://img.shields.io/npm/v/drizzle-cubrid)](https://www.npmjs.com/package/drizzle-cubrid) |

### Go

| Repository | Role | Version | Description | Status |
|---|---|---|---|---|
| **[cubrid-go](https://github.com/cubrid-lab/cubrid-go)** | Driver | v0.2.1 ![beta](https://img.shields.io/badge/-beta-yellow) | Pure Go `database/sql` driver | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/cubrid-go/ci.yml?label=tests)](https://github.com/cubrid-lab/cubrid-go/actions) |
| **[gorm-cubrid](https://github.com/cubrid-lab/gorm-cubrid)** | ORM | v0.1.0 ![alpha](https://img.shields.io/badge/-alpha-red) | GORM dialect for CUBRID | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/gorm-cubrid/ci.yml?label=tests)](https://github.com/cubrid-lab/gorm-cubrid/actions) |

### Rust

| Repository | Role | Version | Description | Status |
|---|---|---|---|---|
| **[cubrid-rs](https://github.com/cubrid-lab/cubrid-rs)** | Driver | v0.1.0 ![alpha](https://img.shields.io/badge/-alpha-red) | Async Rust driver (pure Rust, no FFI) | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/cubrid-rs/ci.yml?label=tests)](https://github.com/cubrid-lab/cubrid-rs/actions) |
| **[sea-orm-cubrid](https://github.com/cubrid-lab/sea-orm-cubrid)** | ORM | v0.1.0 ![alpha](https://img.shields.io/badge/-alpha-red) | SeaORM backend for CUBRID | [![Tests](https://img.shields.io/github/actions/workflow/status/cubrid-lab/sea-orm-cubrid/ci.yml?label=tests)](https://github.com/cubrid-lab/sea-orm-cubrid/actions) |

### Tools & Resources

| Repository | Description | Status |
|---|---|---|
| **[cubrid-cookbook-python](https://github.com/cubrid-lab/cubrid-cookbook-python)** | Production-ready Python examples — quickstarts, migration guides, templates | ![active](https://img.shields.io/badge/-active%20development-yellow) |
| **[cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark)** | Scientific benchmark suite — reproducible experiments, automated comparison | ![active](https://img.shields.io/badge/-active%20development-yellow) |

---

## Roadmap

See the **[Ecosystem Roadmap](https://github.com/cubrid-lab/.github/blob/main/ROADMAP.md)** for cross-repo priorities and timeline.

Track execution on the **[Project Board](https://github.com/orgs/cubrid-lab/projects/2)**.

---

## Getting Started

> **New to CUBRID?** Start with the [Python Cookbook](https://github.com/cubrid-lab/cubrid-cookbook-python) — quickstarts, migration guides, and production templates.

**Choose your language:**

- **Python**: [`sqlalchemy-cubrid`](https://github.com/cubrid-lab/sqlalchemy-cubrid) (ORM), [`pycubrid`](https://github.com/cubrid-lab/pycubrid) (driver), or [`cubrid-mcp-server`](https://github.com/cubrid-lab/cubrid-mcp-server) (MCP/LLM)
- **TypeScript/Node.js**: [`drizzle-cubrid`](https://github.com/cubrid-lab/drizzle-cubrid) (ORM) or [`cubrid-client`](https://github.com/cubrid-lab/cubrid-client) (driver)
- **Go**: [`gorm-cubrid`](https://github.com/cubrid-lab/gorm-cubrid) (ORM) or [`cubrid-go`](https://github.com/cubrid-lab/cubrid-go) (driver)
- **Rust**: [`sea-orm-cubrid`](https://github.com/cubrid-lab/sea-orm-cubrid) (ORM) or [`cubrid-rs`](https://github.com/cubrid-lab/cubrid-rs) (driver)

Each repository includes setup instructions, API documentation, and examples.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../.github/CONTRIBUTING.md) for guidelines.

**Community:**
- 💬 Questions? Post in [GitHub Discussions](https://github.com/orgs/cubrid-lab/discussions)
- 🐛 Found a bug? Open an issue on the relevant repo
- 📝 Have an idea? Start a [Discussion](https://github.com/orgs/cubrid-lab/discussions)
- 📋 Track progress: [Project Board](https://github.com/orgs/cubrid-lab/projects/2) (maintainers only)

---

## License

All projects are licensed under the **MIT License**. See individual repositories for details.

---

## Security

If you discover a security vulnerability, please report it via [GitHub Security Advisories](https://github.com/cubrid-lab/sqlalchemy-cubrid/security/advisories) or email the maintainers. Do not open a public issue. See [SECURITY.md](../.github/SECURITY.md) for details.

---

<div align="center">

_CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project._

Made with ❤️ by the CUBRID Lab team

[GitHub](https://github.com/cubrid-lab) • [Discussions](https://github.com/orgs/cubrid-lab/discussions)

</div>
