# Code Conventions

## File Headers

Start every authored source file with a short purpose header. State what the module owns, what it deliberately does not own when that boundary matters, and the most important lifecycle or safety invariant.

Rust:

```rust
//! Issues and verifies short-lived upload grants.
//!
//! This module owns grant policy and signing, but not object persistence.
//! A grant is always scoped to one workspace and expires within five minutes.
```

TypeScript or TSX:

```ts
/**
 * Owns the project activity stream and reconnect lifecycle.
 * Durable event history remains server-owned; this client keeps only a bounded view.
 */
```

Keep the header concrete. Do not add author names, dates, legal boilerplate, change logs, or generic descriptions such as “utilities.”

## Comments and Documentation

- Add `///` documentation to public Rust types, traits, functions, fields with non-obvious meaning, and externally relevant error variants.
- Document units, time zones, ordering, ownership, retry/idempotency behavior, and whether identifiers are sensitive.
- Add comments before security gates, concurrency invariants, protocol workarounds, and surprising domain rules.
- Explain why a fallback is safe and observable. Do not silently turn dependency failure into success.
- Link a standards document or upstream issue when behavior exists to satisfy an external quirk.
- Update or delete comments when behavior changes. A stale comment is a correctness defect.
- Avoid line-by-line narration, commented-out code, task history, and comments that merely translate syntax into English.

## Rust Style

- Use Rust 2024 for greenfield crates unless the deployment target or workspace requires an older edition.
- Run `cargo fmt`; do not hand-align code against rustfmt.
- Run Clippy with warnings denied for changed targets and features.
- Prefer precise domain types and enums over strings, booleans, and unstructured JSON.
- Write total business functions over precise input types; do not make downstream callers handle cases the domain has already proved impossible.
- Prefer legal state-transition functions that consume a state-specific value and return the next state over a generic status setter.
- Put required state-specific data in the matching enum variant/type; do not represent a domain guarantee with `Option`.
- Keep visibility as narrow as possible. Prefer `pub(crate)` over `pub` for internal sharing.
- Prefer borrowed inputs when ownership is unnecessary; clone handles designed to be cheap rather than wrapping everything in new synchronization.
- Use exhaustive `match` for domain states. Avoid wildcard arms when new variants should force a decision.
- Use iterators when they clarify intent; use ordinary loops when they make control flow or early exits easier to audit.
- Keep functions focused. Extract named helpers when a block mixes policy, IO, formatting, and transport concerns.
- Use `thiserror` for typed reusable errors and `anyhow` for executable composition/context boundaries.
- Never use `unwrap` or `expect` on production request/job paths. Permit them in tests and compile-time/static invariants only when failure truly indicates a programmer or deployment error and the message is specific.
- Do not suppress lints broadly. Scope an allow to the smallest item and explain why it is necessary.

## API and Data Conventions

- Apply [parse-dont-validate.md](parse-dont-validate.md): convert raw values to refined domain or capability types once, then accept those types downstream.
- Use snake_case in Rust and apply an explicit Serde rename policy for external camelCase contracts.
- Version public contracts deliberately and preserve backwards compatibility unless a break is approved.
- Use opaque identifiers and strongly typed wrappers where values from different domains are easy to mix up.
- Normalize once at the boundary, validate before side effects, and store a canonical representation.
- Separate omitted, explicit `null`, and concrete update values when PATCH semantics require all three states.
- Return stable machine-readable error codes plus safe human-readable messages.
- Make timestamps unambiguous and serialized in UTC unless the domain explicitly requires a named local time zone.

## Test and Coverage Standard

- Require at least 95% line coverage for every changed first-party crate or package.
- Measure Rust coverage with `cargo llvm-cov`; add it to CI rather than relying on a developer estimate.
- Gate each independently owned crate/package where practical so a large well-tested module cannot hide a weak one.
- Exclude only generated files, tool-mandated glue, or platform code that cannot execute in the coverage environment. Keep exclusions narrow, reviewed, and documented next to coverage configuration.
- Cover happy paths, boundary values, malformed input, authorization failures, dependency failures, retry/idempotency, and state transitions.
- Add integration tests for route wiring, middleware ordering, persistence transactions, and external contracts.
- For concurrency or live delivery, test disconnects, cancellation, duplicate events, ordering assumptions, and resource cleanup.
- Prefer fakes at owned boundaries and realistic protocol fixtures. Do not mock the unit until the test only proves its own expectations.

Suggested Rust gate:

```text
cargo llvm-cov --all-features --workspace --fail-under-lines 95
```

If the workspace cannot run all features together, define explicit CI coverage jobs for compatible feature sets and enforce the threshold on each relevant crate.

## Review Gate

Before completion, confirm:

- Every new or substantially rewritten source file has a useful header.
- Public and non-obvious contracts are documented.
- Comments explain reasons and invariants, not syntax.
- Formatting, Clippy, tests, and the 95% coverage command pass.
- Coverage exclusions are narrow and justified.
- No warning suppression, fallback, or `unwrap` hides an unhandled production failure.
- Authentication, authorization, identifiers, and validated values cross the boundary as proof-bearing types rather than raw values plus booleans.
- Business rules that Rust can express are enforced by construction and function signatures, with runtime checks restricted to external facts and parsing boundaries.
