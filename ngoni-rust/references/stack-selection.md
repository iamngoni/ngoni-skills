# Stack Selection

Use this guide to select a runtime without forcing a rewrite.

## Decision Table

| Workload | Preferred choice | Notes |
| --- | --- | --- |
| Greenfield HTTP API or internal service | Rust 2024 + Actix Web + Tokio | Use typed state, Serde contracts, tracing, and health/readiness routes. |
| Existing Rust HTTP service | Existing framework | Continue Actix or Axum unless migration is explicitly in scope. |
| Cloudflare edge API | Rust Worker | Keep WASM-compatible dependencies; use D1, Queues, KV, or Durable Objects only for their native strengths. |
| Durable per-entity fan-out | Durable Object + WebSocket | Suitable for ephemeral live project/session channels; persist durable truth elsewhere. |
| One-way progress or event feed | SSE | Add event IDs/cursors, heartbeats, cancellation, and reconnect behavior when needed. |
| Bidirectional live interaction | WebSocket | Define protocol, authentication, readiness, reconnect, and backpressure. |
| Durable background processing | Queue consumer or scheduled worker | Make jobs idempotent and observable; do not depend on an open browser connection. |
| Greenfield full-stack web | TanStack Start + React + TypeScript | Pair with Tailwind CSS and shadcn/ui; use server functions and route boundaries intentionally. |
| Established frontend application | Existing frontend plus narrow Rust services | Extract CPU-heavy, security-sensitive, independently deployable, or reliability-critical work when the boundary is real. |

## Default Rust Dependencies

Select only what the service uses:

- `actix-web`, `tokio`
- `serde`, `serde_json`
- `tracing`, `tracing-subscriber`, optionally OpenTelemetry integration
- `reqwest` with `default-features = false` and Rustls TLS
- `sqlx` for compile-time-oriented PostgreSQL access and pooling
- `redis` for expiring replay/session/coordination state
- `thiserror` for library/domain errors; `anyhow` at application composition boundaries
- `chrono` or `time` for timestamps
- `uuid` for opaque identifiers
- `secrecy`, `subtle`, or a focused constant-time comparison crate where secret handling requires it

Prefer pinned Git revisions over floating branches when a Git dependency is unavoidable. Prefer registry releases when they provide the required behavior.

## Database Choices

- Use PostgreSQL as the default durable relational store.
- Use transactions for multi-step invariants.
- Use migrations committed with the code.
- Use database types that match production, including 64-bit IDs where schemas exceed 32-bit ranges.
- Use Redis for expiry, replay windows, rate limits, coordination, or disposable cache—not as an accidental source of truth.
- Use D1 only inside a Cloudflare-native architecture where its operational tradeoffs fit.

## Frontend Choices

- Use TanStack Start for greenfield routing, SSR, and server/client composition.
- Use TanStack Query when remote-state caching and invalidation add value; avoid wrapping trivial loader data reflexively.
- Use Tailwind CSS tokens for themeable styling.
- Use shadcn/ui as accessible source primitives, then customize composition, density, tokens, and states to the product.
- Prefer Lucide icons when the repository already uses them.

## Reasons to Deviate

Deviate when repository constraints, deployment targets, team ownership, binary size, platform support, or an established service make another choice safer. Record the reason in the implementation summary when it materially affects maintenance.
