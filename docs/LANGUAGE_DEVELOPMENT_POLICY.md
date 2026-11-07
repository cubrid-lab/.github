# Development guidance by language and repository

This page is a **navigation and review guide** for CUBRID Lab contributors.
It does not impose a single tooling version, formatting tool, CI pipeline,
code ownership scheme or release schedule on all projects.

The **owning repository's** actual manifests, contributor/development guide,
verified CI workflow, support matrix and release policy determine the
requirements for any given change. These sources must agree; where they
currently disagree, resolve the discrepancy in the owning repository instead
of treating this page as an authoritative replacement.

For connector API design, see
[language-native connector principles](LANGUAGE_NATIVE_CONNECTORS.md);
for CI test selection, see [change-impact CI policy](CI_CHANGE_IMPACT_POLICY.md).

## Language-appropriate starting points

| Language or domain | Typical commands/tools to check | Important distinctions |
| --- | --- | --- |
| Python libraries | `python -m pytest`, Ruff lint/format, Mypy where configured | Use the dependency groups, lockfiles, markers and Python matrix declared by the project. Offline tests do not prove real CUBRID connectivity |
| TypeScript / Node.js | `npm ci`, `npm test`, `tsc --noEmit`, **the project's selected** ESLint, Biome and/or Prettier commands | Check runtime engines, declaration/API compatibility, framework and peer dependency ranges. Do not assume every repository exposes the same npm scripts |
| Go | `gofmt`/`go fmt`, `go vet`, `go test`, optional `golangci-lint` when required | Confirm `go.mod` minimum, `database/sql` or GORM contracts, module import paths and whether live tests exercise a broker |
| Rust | `cargo fmt --check`, `cargo clippy`, `cargo test` | Confirm each workspace/crate MSRV against `Cargo.toml` and an **actual** minimum-toolchain CI lane. An ignored live test is not covered by an ordinary offline test |
| C/C++ | Repository CMake presets/build targets, native format/warning/compile/test commands | Preserve the upstream engine's compiler conventions, module build design and test practices; do not impose a new generic style policy |
| Java / Gradle | Project Gradle/Ant build and test tasks, JDK toolchain/target checks | The CUBRID engine's PL, JDBC and subprojects have different build and compatibility contracts; use their own instructions |
| Kubernetes Operator (Go) | `go mod`, `make verify`, generated CRD/RBAC checks, controlled Kind/E2E scenarios | Preserve ADRs, native CUBRID HA ownership, scenario evidence, environment boundaries and independent high-risk review |
| Terraform / infrastructure | `terraform fmt -check`, safe `terraform validate`, reviewed `terraform plan` | State locking, credentials, environment isolation, destructive changes and any `apply` need explicit project-specific authorization |
| Documentation, benchmarks and generated assets | MkDocs or HTML build, link checks, benchmark provenance, deterministic generation checks | Use the actual artifact/experiment workflow rather than adding unrelated runtime integration tests |

These are **examples, not required scripts**. A repository may have no
`npm run lint`, `make lint` or dedicated formatter; do not claim those
commands work until you inspect its scripts, Makefile and CI.

## Actual repository development entrypoints

Browse the owning repository first. Some projects use `AGENTS.md`,
`CONTRIBUTING.md`, `docs/DEVELOPMENT.md`, an architecture decision record
or a site-specific runbook for detailed instructions.

| Repository | Scope | Start here |
| --- | --- | --- |
| [pycubrid](https://github.com/cubrid-lab/pycubrid) | Python driver | [Contribution guide](https://github.com/cubrid-lab/pycubrid/blob/main/CONTRIBUTING.md), `pyproject.toml`, `Makefile` |
| [sqlalchemy-cubrid](https://github.com/cubrid-lab/sqlalchemy-cubrid) | Python SQLAlchemy dialect | [Contribution guide](https://github.com/cubrid-lab/sqlalchemy-cubrid/blob/main/CONTRIBUTING.md), `pyproject.toml`, `tox.ini` |
| [cubrid-mcp-server](https://github.com/cubrid-lab/cubrid-mcp-server) | Python MCP server | [Contribution guide](https://github.com/cubrid-lab/cubrid-mcp-server/blob/main/CONTRIBUTING.md), `pyproject.toml`, `Makefile` |
| [cubrid-cookbook-python](https://github.com/cubrid-lab/cubrid-cookbook-python) | Python examples | [Contribution guide](https://github.com/cubrid-lab/cubrid-cookbook-python/blob/main/CONTRIBUTING.md), `Makefile`, `SUPPORT_MATRIX.md` |
| [cubrid-client](https://github.com/cubrid-lab/cubrid-client) | TypeScript CUBRID client | [Contribution guide](https://github.com/cubrid-lab/cubrid-client/blob/main/CONTRIBUTING.md), `package.json`, `docs/API_STABILITY.md` |
| [drizzle-cubrid](https://github.com/cubrid-lab/drizzle-cubrid) | TypeScript Drizzle adapter | [Contribution guide](https://github.com/cubrid-lab/drizzle-cubrid/blob/main/CONTRIBUTING.md), `package.json` |
| [cubrid-go](https://github.com/cubrid-lab/cubrid-go) | Go `database/sql` driver | [Contribution guide](https://github.com/cubrid-lab/cubrid-go/blob/main/CONTRIBUTING.md), `go.mod` |
| [gorm-cubrid](https://github.com/cubrid-lab/gorm-cubrid) | Go GORM adapter | [Contribution guide](https://github.com/cubrid-lab/gorm-cubrid/blob/main/CONTRIBUTING.md), `go.mod` |
| [cubrid-rs](https://github.com/cubrid-lab/cubrid-rs) | Rust driver workspace | [Contribution guide](https://github.com/cubrid-lab/cubrid-rs/blob/main/CONTRIBUTING.md), `Cargo.toml` |
| [sea-orm-cubrid](https://github.com/cubrid-lab/sea-orm-cubrid) | Rust SeaORM adapter | [Contribution guide](https://github.com/cubrid-lab/sea-orm-cubrid/blob/main/CONTRIBUTING.md), `Cargo.toml` |
| [cubrid-benchmark](https://github.com/cubrid-lab/cubrid-benchmark) | Python with optional TypeScript/Go/Rust experiments | [Contribution guide](https://github.com/cubrid-lab/cubrid-benchmark/blob/main/CONTRIBUTING.md), `REPRODUCIBILITY.md` |
| [cubrid-kubernetes-operator](https://github.com/cubrid-lab/cubrid-kubernetes-operator) | Go/Kubernetes Operator | [Contribution guide](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md), `DESIGN.md`, `docs/compatibility.md` |
| [terraform-zadara-k8s](https://github.com/cubrid-lab/terraform-zadara-k8s) | Terraform/Kubernetes lab | [Contribution guide](https://github.com/cubrid-lab/terraform-zadara-k8s/blob/main/CONTRIBUTING.md), `README.md`, `scripts/tfstate.sh` |
| [cubrid](https://github.com/cubrid-lab/cubrid) | C/C++ database engine, Java PL and submodules | [Contribution guide](https://github.com/cubrid-lab/cubrid/blob/develop/CONTRIBUTING.md), `CMakePresets.json`, `pl_engine/AGENTS.md`, `unit_tests/AGENTS.md` |
| [showcase](https://github.com/cubrid-lab/showcase) | HTML presentations and assets | [Contribution guide](https://github.com/cubrid-lab/showcase/blob/main/CONTRIBUTING.md), `DESIGN.md` |
| [cubrid-lab.github.io](https://github.com/cubrid-lab/cubrid-lab.github.io) | Documentation site | [Contribution guide](https://github.com/cubrid-lab/cubrid-lab.github.io/blob/main/CONTRIBUTING.md), `mkdocs.yml` |
| [brand](https://github.com/cubrid-lab/brand) | Generated visual assets | [Contribution guide](https://github.com/cubrid-lab/brand/blob/main/CONTRIBUTING.md), `BRAND_USAGE.md`, `AGENTS.md` |
| [cubrid-lab/.github](https://github.com/cubrid-lab/.github) | Organization policy and templates | [Contribution guide](https://github.com/cubrid-lab/.github/blob/main/CONTRIBUTING.md), `docs/`, `workflow-templates/` |

The links identify **current entrypoints**, not a statement that all
individual policy gaps are already fixed. Each repository owns its own
corrections and review of any contradictory wording.

## Verify claims before writing a support statement

Always distinguish:

1. **Declared compatibility:** language/toolchain minimum in `go.mod`,
   `Cargo.toml`, `package.json` engines, `pyproject.toml`, support
   documentation or dependency constraints.
2. **Executed validation:** exact language versions, CUBRID image/server
   versions, test suites, start/end status and evidence recorded by CI.
3. **Released support:** the published artifact and actually tested
   compatibility contract. A GitHub tag, registry version, source-only
   simulation or proxy/mocked response is not automatically production
   readiness evidence.

A declared lower runtime or framework version is not verified merely
because the latest toolchain builds. Neither high unit-test coverage nor
passing integration job **names** prove a CUBRID connection took place.
Do not rewrite import/module paths or narrow/broaden public dependency
ranges as a cosmetic documentation fix.

For change-dependent PR testing, use the
[CI change-impact policy](CI_CHANGE_IMPACT_POLICY.md) and preserve
security/release checks, verified required statuses, and fail-closed
classification. For published artifacts, follow the owning repository's
release and security policies. This guidance does not create a new
approval, automation or cross-project release dependency.
