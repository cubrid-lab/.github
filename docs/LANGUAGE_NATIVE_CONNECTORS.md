# Language-native CUBRID connectors

CUBRID connectors are maintained as **independent projects**. A shared
database engine does not require shared method names, identical language APIs,
the same driver architecture, or coordinated releases.

## Design principles

1. **Use the host language's conventions.** Match the established
   database interfaces, type and error conventions, cancellation model,
   resource ownership and concurrency semantics of the language.
2. **Preserve database-level meaning.** Given the same CUBRID server
   version, SQL, parameters, schema and relevant session settings, each
   connector should represent values, precision, NULLs, transactions,
   isolation levels and supported CUBRID behaviors correctly.
3. **Allow different representations.** Distinct row types, errors,
   connection defaults, asynchronous interfaces and transaction APIs
   are acceptable when idiomatic and documented. Database correctness
   does not imply identical public APIs.
4. **Treat official drivers as references, not templates.** Use vendor
   documentation, server traces, CCI/JDBC tests and established client
   implementations as evidence. Investigate differences; do not
   reproduce undocumented quirks or defects merely to mirror another
   connector.
5. **Require a reason for extra layers.** Before adding an adapter,
   driver bridge or emulation layer, compare alternatives, user demand,
   correctness constraints, compatibility implications, performance,
   ownership and long-term maintenance.
6. **Keep stewardship local.** Each repository sets its own API,
   support matrix, tests, dependencies, roadmap, release promises
   and review workflow. This document adds no organization-wide
   implementation dependency, test harness, mandatory gate or
   synchronized version schedule.

## Language-native interface examples

These are illustrations, **not mandatory features** for any repository.

| Ecosystem | Relevant conventions |
| --- | --- |
| Python | PEP 249 / DB-API for synchronous clients, Pythonic exceptions, optional async APIs when implemented |
| TypeScript / Node.js | Promise-based operations, typed APIs, Node runtime errors, explicit async resource cleanup |
| Go | `database/sql`, `database/sql/driver`, `context.Context`, error values and explicit transaction handling |
| Rust | `Result`, typed errors, ownership and lifetime constraints, ecosystem-appropriate sync or async clients |

An ORM integration or framework adapter also follows **its upstream framework's
contract**; a Python dialect, TypeScript query builder, Go GORM adapter and
Rust SeaORM proxy need not share internal structure or release versions.

## Review a proposed connector feature

For a proposed public API, protocol behavior, adapter or compatibility layer,
check the following in the owning repository:

- **User value:** Which real use case is enabled? What problem does an
  existing language-native facility fail to solve?
- **Idiomatic design:** Does the interface fit the expected conventions
  of this particular language or framework?
- **CUBRID correctness:** What server behavior is documented, and what
  same-version database evidence tests values, SQL execution, errors,
  concurrency and transaction effects?
- **Complexity:** Is a new abstraction needed? Can a simpler or
  existing language-native mechanism meet the same need?
- **Compatibility:** What do this repository's supported runtime,
  dependency, versioning and migration promises require?
- **Maintenance:** Who will own the tests, docs, security issues and
  future upstream compatibility changes?

Record the answer and tests **in the repository that owns the feature**.
Do not infer supported database versions from a source dependency range,
a green offline build, or another connector's release notes.

This guidance is conceptual only. It does not modify source code,
impose shared implementation work, or override repository-specific
review, security, licensing, or release requirements.
