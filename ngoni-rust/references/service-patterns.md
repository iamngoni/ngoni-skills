# Service Patterns

Apply [code-conventions.md](code-conventions.md) to every file and test described here.

## Project Shape

For a non-trivial Actix service, prefer modules that expose intent rather than technical buckets alone:

```text
src/
  main.rs          process wiring and lifecycle
  config.rs        typed environment configuration
  state.rs         shared cloned clients and service state
  error.rs         internal errors and API mapping
  routes/          transport handlers and route registration
  domain/          business rules and types
  services/        application workflows
  repositories/    persistence boundaries
  clients/         outbound service adapters
```

Use a smaller shape for a small service. Do not create empty layers.

## HTTP Boundaries

- Register routes in an obvious, auditable place.
- Deserialize into narrow wire structs, parse them into valid domain types, and expose only the domain types beyond the boundary.
- Use request extractors or boundary middleware that yield `AuthenticatedUser` or a narrower authorization capability. Do not make handlers inspect authentication booleans.
- Authorize resource access before expensive dependency calls; carry the result as a resource-scoped proof type.
- Return stable JSON error codes/messages without internal stack details.
- Apply body-size limits, timeouts, CORS, and cache policy intentionally.
- Put session and identity endpoints behind `Cache-Control: no-store`.
- Expose liveness separately from readiness when dependency health matters.

## State and Concurrency

- Construct config, pools, Redis clients, and HTTP clients once at startup.
- Put clone-cheap handles in `web::Data` or equivalent shared state.
- Avoid holding locks across `.await`.
- Bound spawned tasks and retain cancellation or join handles when lifecycle matters.
- Use channels with deliberate capacity and documented overflow behavior.
- Keep blocking or CPU-heavy work off async executor threads.
- Encode legal in-memory lifecycle transitions with state-specific types or exhaustive transition methods; back cross-process invariants with transactions and database constraints.

## Errors

- Use typed domain errors where callers need to branch.
- Attach context when crossing IO or service boundaries.
- Avoid `unwrap` and `expect` in request paths. They are acceptable in tests and truly static startup invariants when the failure message is precise.
- Log an internal correlation/request ID and return it when operator follow-up benefits.

## Outbound HTTP

- Use one shared Reqwest client with connect and total timeouts.
- Use Rustls unless platform constraints require another TLS backend.
- Validate response status and bound response bodies.
- Retry only idempotent or explicitly idempotency-keyed operations.
- Add exponential backoff with jitter and a hard attempt/deadline cap.
- Never allow user input to become an arbitrary internal URL without allowlisting and URL validation.

## Persistence and Writes

- Parameterize every query.
- Scope writes to exact identifiers and verify affected-row counts.
- Keep production investigations read-only until a write is explicitly approved.
- Make jobs and externally retried mutations idempotent.
- Record audit events for sensitive operational writes.
- Never use a broad update/delete as a shortcut.

## SSE

- Set `Content-Type: text/event-stream`, disable buffering where the proxy requires it, and avoid caching.
- Emit structured named events rather than untyped text blobs.
- Give replayable events monotonically increasing IDs/cursors.
- Support `Last-Event-ID` or an explicit `after` cursor when the store can replay.
- Send periodic comments or heartbeat events to keep intermediaries alive.
- Detect disconnects, release resources, and stop upstream work when appropriate.
- Keep durable job state separate from the stream.

## WebSockets

- Authenticate the upgrade and scope the channel to the authorized entity.
- Send a ready/hello frame so the client can distinguish connection from useful readiness.
- Validate incoming frames and ignore or close on protocol violations deliberately.
- Bound fan-out and message size; define slow-consumer behavior.
- Let clients reconnect with capped exponential backoff.
- Treat ephemeral fan-out as ephemeral unless persistence is explicitly implemented.

## Observability

- Initialize tracing before starting the server and keep telemetry guards alive for process lifetime.
- Instrument HTTP requests and propagate W3C trace context when services participate in distributed traces.
- Log service, route, status, latency, and safe business context.
- Prefer metrics for rates/latencies and traces for causal debugging.
- Do not put tokens, raw applicant/customer identifiers, payload bodies, or credentials into telemetry.

## Tests

- Unit-test pure domain decisions and normalization at the module boundary.
- Test handlers for success, invalid input, unauthenticated/unauthorized access, and dependency failure.
- Test raw-to-refined conversion and capability extraction so downstream code never needs to re-test validity or authentication flags.
- Test database invariants with realistic migrations when feasible.
- Test SSE reconnect/cursor semantics and cancellation.
- Test WebSocket readiness, malformed messages, disconnect, and reconnect behavior.
- Keep tests deterministic: control time, random seeds, and external clients.
- Measure coverage with `cargo llvm-cov`; require at least 95% line coverage in each changed first-party crate.
- Do not use coverage as a substitute for assertions, boundary cases, mutation resistance, or end-to-end contract proof.
