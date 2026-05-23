# CUBRID Labs — Ecosystem Roadmap

> **Last updated**: 2026-05-23
>
> This is the unified roadmap for the cubrid-labs ecosystem.
> Milestones are authoritative for "next release" scope.
> This document is authoritative for direction, priorities, and cross-repo dependencies.
>
> 📋 [**Org Project Board**](https://github.com/orgs/cubrid-lab/projects/2) · See [individual repo milestones](#release-focus-by-repo) for execution details.

---

## Ecosystem Map

```mermaid
graph TD
    subgraph Drivers["🔌 Drivers"]
        pycubrid["pycubrid (Python)\nv1.5.0"]
        cubrid_client["cubrid-client (TypeScript)\nv1.1.0"]
        cubrid_go["cubrid-go (Go)\nv0.2.1"]
        cubrid_rs["cubrid-rs (Rust)\nv0.1.0"]
    end

    subgraph ORMs["🏗️ ORMs & Dialects"]
        sqlalchemy["sqlalchemy-cubrid\nv1.5.0"]
        drizzle["drizzle-cubrid\nv0.2.1"]
        gorm["gorm-cubrid\nv0.1.0"]
        sea_orm["sea-orm-cubrid\nv0.1.0"]
    end

    subgraph Meta["📚 Meta"]
        cookbook_py["cubrid-cookbook-python ✅"]
        benchmark["cubrid-benchmark"]
    end

    pycubrid --> sqlalchemy
    cubrid_client --> drizzle
    cubrid_go --> gorm
    cubrid_rs --> sea_orm

    sqlalchemy --> cookbook_py
    drizzle -.-> cookbook_ts["cubrid-cookbook-typescript\n(planned)"]
    gorm -.-> cookbook_go["cubrid-cookbook-go\n(planned)"]
    sea_orm -.-> cookbook_rs["cubrid-cookbook-rust\n(planned)"]

    pycubrid --> benchmark
    cubrid_client --> benchmark
    cubrid_go --> benchmark
    cubrid_rs --> benchmark
```

---

## Now / Next / Later

### 🟢 Now (Current Focus)

- **cubrid-cookbook-python ✅ COMPLETE** — 55+ production-ready recipes (pycubrid, SQLAlchemy, Pandas, Flask, FastAPI, Streamlit, Django). Tested on CUBRID 11.2 + 11.4. [Support Matrix](https://github.com/cubrid-lab/cubrid-cookbook-python/blob/main/SUPPORT_MATRIX.md)
- **Python driver improvements** — pycubrid v1.5.0 (async TLS hardening with STARTTLS, transport contract lock — session restore + mid-fetch reconnect handling, Python 3.10 async-TLS preflight verification probe, 1.x release policy with `compat-check` CI gate); sqlalchemy-cubrid v1.5.0 (SQLAlchemy 2.1/2.2 forward-compat shims — `update_post_criteria_clause`, `Float` numeric affinity, async `await_` staticmethod; async integration stability)
- **Performance profiling & optimization** — Python driver optimized (19% fetch improvement); query compilation cache added to sqlalchemy-cubrid. Ongoing: further gap reduction vs MySQL.
- **Benchmark automation** — Nightly CI runs with extended workloads (connect/disconnect, prepared statements, batch insert, concurrent select)
- **cubrid-rs protocol completion** — Broker handshake, authentication, query execution (v0.2.0)

### 🟡 Next (1–3 Months)

- **Language-specific cookbooks** — TypeScript (cubrid-cookbook-typescript), Go (cubrid-cookbook-go), Rust (cubrid-cookbook-rust) following the Python cookbook pattern
- **v1.0 stabilization** — API freeze for cubrid-go, gorm-cubrid, drizzle-cubrid
- **Connection resilience** — Retry policies, connection health checks (cubrid-client v1.2.0)
- **Registry publishing** — crates.io (cubrid-rs, sea-orm-cubrid); PyPI Trusted Publisher configured ✅ (pycubrid v1.5.0, sqlalchemy-cubrid v1.5.0 published)

### 🔵 Later (3–6 Months)

- **JSON type mapping** — CUBRID supports JSON since 10.2; map in sqlalchemy-cubrid, pycubrid, cubrid-client
- **Async driver for Rust** — cubrid-tokio with backpressure handling (cubrid-rs v0.5.0)
- **Connection pool crates** — cubrid-pool for Rust (cubrid-rs v0.6.0)
- **Full SeaORM feature parity** — Entity generation, migrations, crates.io availability
- **Ecosystem documentation portal** — Unified docs site (GitHub Pages)

---

## Dependency Graph

```mermaid
graph LR
    subgraph "Must stabilize first"
        A[pycubrid v1.0.0]
        B[cubrid-go v1.0.0]
        C[cubrid-rs v0.2.0]
        D[cubrid-client v1.2.0]
    end

    subgraph "Depends on driver stability"
        E[sqlalchemy-cubrid v0.8.0]
        F[gorm-cubrid v1.0.0]
        G[drizzle-cubrid v1.0.0]
        H[sea-orm-cubrid v1.0.0]
    end

    subgraph "Depends on all above"
        I[cubrid-cookbook v1.0]
        J[cubrid-benchmark v1.0]
    end

    A --> E
    B --> F
    C --> H
    D --> G
    E --> I
    F --> I
    G --> I
    H --> I
    A --> J
    B --> J
    C --> J
    D --> J
```

---

## Release Focus by Repo

| Repo | Next Milestone | Focus | Link |
|------|---------------|-------|------|
| **pycubrid** | v1.5.0 ✅ | Async TLS hardening (STARTTLS, Py3.10 preflight probe), transport contract lock, 1.x release policy with `compat-check` CI gate | [Releases](https://github.com/cubrid-lab/pycubrid/releases) |
| **pycubrid** | [v2.0.0](https://github.com/cubrid-lab/pycubrid/milestone/1) | Next major — connection pooling, breaking changes deferred from 1.x | [Milestones](https://github.com/cubrid-lab/pycubrid/milestones) |
| **sqlalchemy-cubrid** | v1.5.0 ✅ | SQLAlchemy 2.1/2.2 forward-compat shims, async integration stability, `sqlalchemy-22-canary` job promoted to gating | [Releases](https://github.com/cubrid-lab/sqlalchemy-cubrid/releases) |
| **sqlalchemy-cubrid** | [v2.0.0](https://github.com/cubrid-lab/sqlalchemy-cubrid/milestone/2) | SA 2.2 full GA support, JSON type mapping | [Milestones](https://github.com/cubrid-lab/sqlalchemy-cubrid/milestones) |
| **cubrid-client** | [v1.2.0](https://github.com/cubrid-lab/cubrid-client/milestone/1) | Reliability & performance | [Milestones](https://github.com/cubrid-lab/cubrid-client/milestones) |
| **drizzle-cubrid** | [v1.0.0](https://github.com/cubrid-lab/drizzle-cubrid/milestone/1) | Stable release | [Milestones](https://github.com/cubrid-lab/drizzle-cubrid/milestones) |
| **cubrid-go** | [v1.0.0](https://github.com/cubrid-lab/cubrid-go/milestone/1) | Stable release | [Milestones](https://github.com/cubrid-lab/cubrid-go/milestones) |
| **gorm-cubrid** | [v1.0.0](https://github.com/cubrid-lab/gorm-cubrid/milestone/1) | Stable release | [Milestones](https://github.com/cubrid-lab/gorm-cubrid/milestones) |
| **cubrid-rs** | [v0.2.0](https://github.com/cubrid-lab/cubrid-rs/milestone/1) | Protocol completeness | [Milestones](https://github.com/cubrid-lab/cubrid-rs/milestones) |
| **cubrid-rs** | [v1.0.0](https://github.com/cubrid-lab/cubrid-rs/milestone/2) | Stable release | [Milestones](https://github.com/cubrid-lab/cubrid-rs/milestones) |
| **sea-orm-cubrid** | [v1.0.0](https://github.com/cubrid-lab/sea-orm-cubrid/milestone/1) | Stable release | [Milestones](https://github.com/cubrid-lab/sea-orm-cubrid/milestones) |
| **cubrid-cookbook-python** | ✅ Complete | 55+ recipes, tested CUBRID 11.2+11.4 | [Repo](https://github.com/cubrid-lab/cubrid-cookbook-python) |
| **cubrid-benchmark** | [v1.0](https://github.com/cubrid-labs/cubrid-benchmark/milestone/1) | Comprehensive benchmarks | [Milestones](https://github.com/cubrid-labs/cubrid-benchmark/milestones) |

---

## Contributing

We welcome contributions to any repo in the ecosystem!

- 🐛 **Found a bug?** Open an issue on the relevant repo
- 💡 **Have a feature idea?** Start a [Discussion](https://github.com/orgs/cubrid-labs/discussions)
- 🔧 **Want to contribute code?** See [CONTRIBUTING.md](CONTRIBUTING.md) and look for `good first issue` labels
- 📋 **Track progress**: [Org Project Board](https://github.com/orgs/cubrid-labs/projects/2)

---

> **Disclaimer**: This roadmap reflects current intentions and priorities. Timelines and scope may change based on community feedback, contributor availability, and technical discoveries. Milestones on individual repos are the most up-to-date source for release planning.
