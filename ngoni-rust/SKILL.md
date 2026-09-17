---
name: ngoni-rust
description: Design, implement, review, or extend Ngoni-style production applications with Rust backends and modern TypeScript frontends. Use for greenfield architecture, Rust HTTP services, Actix Web APIs, Cloudflare Workers, async jobs, SSE or WebSocket features, PostgreSQL/Redis integrations, TanStack Start applications, Tailwind CSS and shadcn/ui frontends, Rust service extraction, parse-don't-validate modeling, authentication and authorization types, code-convention decisions, documentation standards, testing strategy, or stack choices in existing repositories.
---

# Ngoni Rust

Build the smallest production architecture that fits the workload. Prefer Rust for backend ownership, explicit boundaries, typed contracts, observable operations, and evidence-backed delivery.

## Start With Repository Truth

Before choosing or changing a stack:

1. Read the nearest `AGENTS.md` and project instructions completely.
2. Inspect manifests, lockfiles, deployment config, adjacent services, tests, and recent history.
3. Preserve an established framework unless the requested outcome justifies migration.
4. Identify the runtime boundary: ordinary server, edge/WASM, scheduled worker, queue consumer, CLI, or browser app.
5. State consequential assumptions before implementation.

Do not replace working Axum, Vite, or Cloudflare Worker surfaces merely to match the greenfield default. Integrate through narrow contracts and migrate only when explicitly justified.

## Choose the Stack

Use [references/stack-selection.md](references/stack-selection.md) whenever architecture or framework selection is part of the task.

Default greenfield stack:

- Backend: Rust 2024, Tokio, Actix Web.
- Frontend: TanStack Start, React, strict TypeScript, Tailwind CSS, shadcn/ui.
- Persistence: PostgreSQL with SQLx; add Redis only for expiring, shared, or coordination state.
- HTTP clients: Reqwest with Rustls, explicit connect and total timeouts.
- Contracts: Serde request/response types; validate at the boundary.
- Operations: `tracing`, structured logs, health/readiness routes, graceful shutdown.

Choose Cloudflare Workers instead of Actix for edge/WASM workloads already shaped around Workers, D1, Queues, or Durable Objects. Choose the existing framework for an established service unless a migration is part of the task.

## Design the Service

Read [references/service-patterns.md](references/service-patterns.md) before implementing HTTP, persistence, authentication, background work, or live delivery.

Keep these boundaries visible:

1. Parse, authenticate, and authorize at the transport boundary into types that prove those checks succeeded.
2. Put business decisions in testable domain/application functions.
3. Keep storage and external APIs behind narrow modules or traits when substitution is useful.
4. Map internal failures to a stable, non-sensitive API error shape.
5. Inject cloned shared clients/config through application state; do not rebuild them per request.
6. Bound network calls, payloads, retries, fan-out, and queues.

Prefer direct code over speculative abstraction. Extract a shared layer after a real second use or when isolation is required for correctness or testing.

## Parse, Don't Validate

Read [references/parse-dont-validate.md](references/parse-dont-validate.md) before designing authentication, authorization, request DTOs, identifiers, state machines, or domain values.

- Convert untrusted data once at the boundary into a type that can only represent valid state.
- Encode business rules in function signatures and data constructors so illegal calls and state transitions fail to compile wherever Rust can express the invariant.
- Make handlers accept `AuthenticatedUser`, `ProjectMember`, `CanManageProject`, or another capability-bearing type directly. Do not accept a nullable/raw user and branch on `user.is_authenticated`, `user.is_admin`, or equivalent boolean flags.
- Keep validated fields private and expose fallible constructors, `TryFrom`, Serde adapters, or framework extractors.
- Use non-empty collections, maps with unique keys, enums, newtypes, and state-specific types instead of partial functions, correlated booleans, magic strings, duplicate-prone lists, and partially valid structs.
- Put exactly the data guaranteed by a state inside that state's variant/type. If completion requires an artifact, `Completed` contains `VerifiedArtifact`; it does not contain `Option<Artifact>`.
- Make business operations total over their accepted types. Strengthen the input type instead of returning “impossible” `Option`/error branches from downstream code.
- Keep authorization request-scoped and resource-scoped. Re-authorize inside the write transaction when concurrent permission changes can invalidate the proof.
- Treat frontend refinement as a correctness aid, never as the server's authorization boundary.

## Follow the Code Conventions

Read [references/code-conventions.md](references/code-conventions.md) before creating or substantially editing source files.

- Start every authored source file with a concise header comment that explains its purpose, ownership boundary, and important safety or lifecycle constraint. Use Rust inner doc comments (`//!`) for Rust module headers and a short documentation block for TypeScript/TSX.
- Document public APIs and any behavior whose contract is not obvious from its type.
- Comment invariants, authorization boundaries, failure handling, external-system quirks, and the reason for surprising choices.
- Do not narrate syntax or restate a clear function name. Keep comments current in the same change as the code.
- Prefer small cohesive modules, explicit names, narrow visibility, immutable values, typed state, and early validation.
- Make invalid states unrepresentable and pass proof-bearing types beyond the boundary instead of repeatedly checking raw values.
- Treat warnings as failures. Do not leave `todo!`, `unimplemented!`, silent fallback behavior, or production-path `unwrap`/`expect` calls.

## Add Live Delivery Deliberately

Do not add realtime transport when polling or request/response is enough.

- Use SSE for one-way progress, run events, logs, or approval/status streams. Give events stable IDs or cursors when reconnect/replay matters, send heartbeats through proxies, and support cancellation.
- Use WebSockets for bidirectional interaction or high-frequency fan-out. Define ready, reconnect, stale-connection, and malformed-message behavior.
- Use queues for durable asynchronous work. A live stream reports progress; it must not be the only record of durable work.

Make the client reconnect with bounded exponential backoff, clean up on unmount, and avoid duplicating events after reconnect.

## Build the Frontend

For greenfield web work:

1. Use TanStack Start for routing and server/client boundaries.
2. Use TanStack Query for remote server state when caching, invalidation, or mutations warrant it.
3. Use Tailwind CSS and shadcn/ui primitives, adapting tokens to the product rather than shipping stock-demo styling.
4. Keep URL state, loading, empty, error, disabled, and permission states explicit.
5. Share typed API contracts or generated clients when practical; never duplicate silent assumptions across Rust and TypeScript.
6. Preserve accessibility: semantic elements, keyboard access, visible focus, labels, and reduced-motion behavior.

If the repository already uses another frontend stack, follow its conventions and introduce these tools only when requested or when adding an isolated greenfield surface.

## Apply Safety and Operations Gates

- Default investigations to read-only behavior.
- Require explicit authorization for production writes and scope every write to exact records.
- Never hard-delete operational data when a domain soft-delete exists.
- Compare secrets in constant time where relevant; never log secrets, tokens, session material, or sensitive personal data.
- Use least-privilege capabilities rather than arbitrary SQL, URL, path, or method access.
- Make auth/session responses non-cacheable.
- Keep deployment configuration aligned with typed runtime config and fail clearly on missing required values.
- Emit structured context that helps operate the service without exposing customer data.

## Verify in Layers

Run the narrowest relevant checks first, then broaden:

```text
cargo fmt --all -- --check
cargo check --all-targets
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets
cargo llvm-cov --all-features --workspace --fail-under-lines 95
```

Maintain at least 95% line coverage for first-party production code in every changed crate or package. Do not average a poorly tested package into a large workspace total. Use narrowly documented exclusions only for generated code, tool-required glue, or demonstrably unreachable platform shims. Add branch and integration tests where line execution alone does not prove behavior.

Adapt commands to the workspace and feature matrix. For frontends, run the repository's typecheck, unit tests, coverage gate at 95% or higher, and production build. For a changed API, verify success, validation failure, auth failure, and dependency failure. For live delivery, verify reconnect, cleanup, ordering or deduplication, and cancellation.

Do not claim runtime, deployment, or device proof from compilation alone. Report exactly what was and was not exercised.

## Finish the Work

Before handoff:

1. Remove mock, demo, or hardcoded fallback behavior from the touched production path and directly related helpers.
2. Run formatting and focused checks, then the feasible broader suite.
3. Review the diff for accidental scope, secrets, generated noise, and compatibility breaks.
4. Confirm raw authentication, authorization, and validation flags have not leaked past their boundary when a refined type can carry the guarantee.
5. Summarize the architecture choice, behavior changed, proof gathered, and remaining unverified boundary.
