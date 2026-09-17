# Parse, Don't Validate

Turn checks and business rules into types. After a boundary accepts data, downstream code should receive a value whose construction proves the required invariant. Base this practice on Alexis King's [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/): preserve what a check learned in the return type instead of discarding it as `()` or a boolean.

## Core Rule

Avoid this shape:

```rust
async fn account(user: User) -> HttpResponse {
    if !user.is_authenticated {
        return HttpResponse::Unauthorized().finish();
    }
    // The rest of the function must remember the check happened.
}
```

Prefer this shape:

```rust
async fn account(user: AuthenticatedUser) -> HttpResponse {
    // Construction of AuthenticatedUser proves authentication succeeded.
}
```

Implement `AuthenticatedUser` as an Actix extractor or have authentication middleware insert a private, verified principal that the extractor consumes. Reject missing, expired, malformed, or revoked credentials before invoking the handler.

## Boundary Flow

Use this flow consistently:

```text
untrusted bytes
  -> wire/credential type
  -> parse + authenticate + authorize
  -> refined domain/capability type
  -> application service
```

- Keep wire DTOs close to transport code.
- Normalize and validate during conversion, not in every consumer.
- Keep refined-type fields private so invalid instances cannot be assembled with struct literals.
- Use `TryFrom`, smart constructors, custom Serde deserializers, or framework extractors for fallible construction.
- Return specific parse/authentication/authorization errors and map them to safe transport errors at the boundary.

## Compile-Time Business Rules

Design business functions for the representation they require, not the raw representation they happen to receive.

Prefer:

```rust
fn primary_recipient(recipients: NonEmpty<Recipient>) -> &Recipient;
fn calculate_allocations(weights: NonEmpty<PositiveWeight>) -> Allocation;
fn start(job: QueuedJob, worker: AvailableWorker) -> RunningJob;
fn complete(job: RunningJob, artifact: VerifiedArtifact) -> CompletedJob;
```

over:

```rust
fn primary_recipient(recipients: &[Recipient]) -> Option<&Recipient>;
fn start(job: Job) -> Result<Job, InvalidStatus>;
fn complete(job: Job, artifact: Option<Artifact>) -> Result<Job, Error>;
```

The stronger signatures remove impossible branches from implementations and force callers to supply proof. If a parser or transition stops producing the strong type, downstream call sites must fail to compile.

Use Rust's type system to encode rules with:

- `NonEmpty<T>` or an equivalent private-head-plus-tail type for required collections;
- `BTreeMap`/`HashMap` or a domain map when duplicate keys are illegal;
- enums for mutually exclusive states and variants with state-specific data;
- private-field newtypes for bounded, canonical, non-zero, or domain-specific values;
- distinct identifier types to prevent cross-domain mix-ups;
- typestate structs or state-specific owned types when transitions consume one state and produce another;
- capability types when an operation requires authenticated or authorized authority.

Give every state exactly its valid data. Do not use one wide record whose fields become conditionally meaningful:

```rust
enum Job {
    Queued { core: JobCore },
    Running { core: JobCore, started_at: DateTime<Utc> },
    Completed { core: JobCore, artifact: VerifiedArtifact },
    Failed { core: JobCore, failure: JobFailure },
}
```

If the domain says a completed job always has an artifact, `Option<Artifact>` inside `Completed` weakens the rule and recreates an illegal state. Use `Option` only when absence is genuinely valid for that exact variant.

Make transition functions consume the old state when reuse would be invalid. Prefer a total transition API per legal edge over one generic `set_status` method that accepts every state pair.

Do not force compile-time encoding beyond what Rust can honestly prove. Facts from clocks, databases, credentials, and concurrent permissions are runtime inputs: parse them into a proof-bearing type at the trusted boundary, limit that proof's scope/lifetime, and back durable invariants with database constraints and transactions.

## Authentication and Authorization

Model authentication and authorization separately:

- `AuthenticatedUser` proves a current credential resolved to an active principal.
- `ProjectMember` proves the principal can read one identified project.
- `CanManageProject` proves the principal can perform management operations on one identified project.
- `InternalOperator` proves a separately controlled internal capability.

Prefer the narrowest type required by the operation. Do not add `is_admin`, `is_internal`, `is_authenticated`, or permission booleans to a general user struct and expect every handler to interpret them correctly.

Capability types must be:

- request-scoped and non-serializable;
- constructed only by trusted authorization code;
- bound to the exact resource and action they authorize;
- free of reusable bearer secrets;
- re-evaluated at the transactional write boundary if permission can change concurrently.

Do not confuse parsing with caching authorization forever. A proof is valid only for the scope and lifetime encoded by its type and construction path.

## Domain Values

Replace primitive values with refined types when invalid values create meaningful risk:

```rust
pub struct WorkspaceId(Uuid);
pub struct CanonicalEmail(String);
pub struct Percentage(u8);
pub enum JobStatus { Queued, Running, Succeeded, Failed, Cancelled }
```

- Parse `Percentage` once and guarantee `0..=100` internally.
- Parse and canonicalize email/URL/identifier values before storage or comparison.
- Use enums instead of status strings.
- Use distinct types for identifiers from different domains even when both wrap `Uuid` or `i64`.
- Model mutually exclusive state with enums rather than several correlated booleans.
- Use state-specific structs or transition methods when only some fields exist in particular lifecycle states.
- Move state-dependent fields into the variants/types where they are required; do not leave them optional on a shared catch-all struct.
- Prefer `NonZero*` numeric types, non-empty collections, and maps whose structure already enforces the business rule.
- Avoid public constructors or `Default` implementations that can manufacture an invalid domain value.

Do not create wrappers for every primitive. Refine values when doing so removes repeated checks, prevents domain mix-ups, or encodes a security/correctness guarantee.

## Request DTOs and PATCH Semantics

Separate wire types from domain commands:

```text
UpdateProjectRequest -> TryFrom -> UpdateProjectCommand
```

The wire type may represent omitted fields and explicit `null`. The parsed command must represent only valid operations. Preserve three-state PATCH semantics with a dedicated enum or nested option rather than losing intent during deserialization.

Reject unknown or contradictory combinations before calling application services. Do not pass a partially validated request object into the domain layer.

## TypeScript Boundary

Parse API responses, URL/search state, storage values, and form submissions with a schema or explicit parser before treating them as domain values. Use discriminated unions and branded/opaque identifiers where they prevent invalid combinations or ID mix-ups.

Frontend types do not authorize anything. The server must independently construct its own authenticated and authorized capability types.

## Tests and Review

Test:

- every rejection path in the raw-to-refined conversion;
- successful canonicalization and construction;
- expired, revoked, malformed, and missing credentials;
- wrong-resource and wrong-action authorization;
- concurrent permission revocation where a transaction must re-authorize;
- legal and illegal domain state transitions;
- serialization boundaries so proof/capability types cannot leak.
- compile-fail cases for critical typestate/capability APIs when their misuse must remain impossible.

During review, search for boolean or repeated validation smells such as:

```text
is_authenticated
is_authorized
is_admin
is_valid
validate(
permission ==
role ==
set_status
Result<(),
```

Each match is a prompt to ask whether a refined type, enum, extractor, non-empty collection, map, typestate transition, or capability should carry the guarantee instead. Treat validators whose primary output is `()` with suspicion: return the refined value that preserves the proof. Keep a boolean only when it represents genuine domain data rather than evidence that a boundary check succeeded.
