# 1. Clarity and Readability

**Summary instruction:** “Enforce crystal-clear naming, signatures and structure”

## Focus on

* Use the smallest complete change: reuse suitable project code and conventions, then platform features, then installed dependencies; do not add a dependency for a few lines.
  Update affected callers, tests, fixtures, configuration and exports.
* Reduce lines where possible without harming readability.
* Variable naming (intent-revealing; avoid ambiguous 'current' for incoming data; remove need for comments/docstring from great variable/function naming)
* Reduce cyclomatic complexity, make functions short and break them down into smaller ones
* No duplicate code, spot repeated logic and extract it, refactor code
* DRY & complexity (remove dupes; simplify nesting; small helpers and suitable project-declared library or language features)

## Also pay attention to following specific cases

* Method naming sanity check (verbs for actions; describe functional outcomes over implementation details; nouns for factories/getters; intent differs for overloads)
* No work in arguments (at most one method call in callsite; extract locals); -- Examples OK: o.m (a,b,c); o.m (o.m2 ()); o.m (o.m2 ()); -- Examples NOT OK: o.m (o.m2 ().m3 ());
  o.m (o.m2 (), b); o.m (new B ());
* Consistent attribute scope (don’t rebrand visibility; use accessors)
* API noise & parameter hygiene (no catch-all `Map<String,Object>`/varargs; prefer explicit params/DTOs)
* Parameter hygiene (flag overly flexible kwargs/parameters; recommend scoped args)
* Eliminate redundancy ruthlessly (default to deletion; remove dead code/wrappers)
* Inline a private one-call-site helper/function that only returns, forwards, or constructs one expression. Keep it only when it enforces a non-obvious domain invariant, implements
  a required API/override/callback, isolates an unstable boundary, or has multiple real call sites.
* Parameter Mutation & Side Effects:
  -- Hidden Parameter Mutation (signal in name/contract or make pure)
  -- Static Method Purity (pure unless explicitly side-effecting)
  -- Command-Query Separation (split mutators and queries)
  -- Caller Surprise (no hidden behaviors)
* **Comments & Documentation Hygiene**:
  -- Self-documenting code over comments (prefer clear naming that eliminates need for comments)
  -- Apply the writing style loaded by the canonical skill when reviewing technical prose.
* **Intent-to-Implementation Consistency [HIGH PRIORITY]**:
  -- Verify that declared intent (class/test names, docstrings, constants, fixture names, parser names, and test data labels) matches actual implementation/configuration. -- Flag
  any semantic mismatch where code behavior targets a different domain/source/mode/entity than the identifiers and documentation claim. -- Required cross-checks:
    - Naming/docs intent vs runtime config objects (e.g., metadata enums, parser/strategy selected)
    - Fixture/sample identifiers vs actual dataset/source used
    - Assertion wording vs behavior being validated -- Treat as maintainability + correctness risk even if tests pass, because it creates false confidence and misleads future
      refactors. -- Require one of two fixes: align implementation to declared intent, or rename/re-document tests and fixtures to match true behavior. -- Example subcase:
      `TestM7...` / "M7 ... parser" while using `DataSource.NP`.

# 2. Design, Abstractions & Extensibility (SOLID)

**Summary instruction:** “Prefer small, composable designs; kill redundancy; use polymorphism/DI when it reduces complexity; reuse suitable extension points.”

* Modularity & SRP (single responsibility; loose coupling; DI over `new`)
* SOLID & extensibility (use interfaces for real polymorphism; use concrete classes with DI for one production implementation, including external boundaries; avoid monoliths; Law of Demeter)
* Pattern Selection (strategy/template vs generic helpers)
* Naming sanity check:
  -- Name things by their actual responsibility, not by a design-pattern label. -- Use `Builder` only for state-accumulating/fluent builders ending in `build()`. -- Use `Factory`
  only when creation policy, dependencies, polymorphism, lifecycle, or pass-around creation is involved. -- Use `create`, `of`, `from`, or a domain verb for simple local
  creation/conversion. -- Flag one-shot helpers, calculators, parsers, loaders, and orchestrators named as `Builder`/`Factory` when the name adds pattern noise instead of meaning.
* Abstraction Costs / Over-Engineering (HIGH PRIORITY):
  -- Registry/Selector/Strategy/Factory abstractions normally require at least 3 already-implemented production variants. Strategy may also be used for 2 already-real production
  behaviors when it eliminates behavior-selector flags or duplicated dispatch/type switches and supports SRP and OCP. Require a concrete current reason and evidence; speculative,
  test-only, or artificial variants do not count. -- Do not introduce an interface for only one production implementation; mocks, fakes and test subclasses
  do not justify an interface -- Flag delegation chains (A→B→C) where A could call C directly -- Flag unrequested "future-proofing" for cases not currently in the codebase -- Use
  phrase "cognitive overhead" or "unnecessary indirection" when flagging these issues
* **Avoid single-method wrapper classes**:
  -- The implementation must merge a class into its caller when the class exposes one public operation, merely forwards or computes a simple expression, and owns no configuration,
  state, resources, lifecycle, invariants, transaction boundary, or stable domain identity, and is not a justified polymorphic variant.
  -- The implementation must keep a class with one public operation when its instance represents a named component and owns any of those responsibilities. A single public
  operation does not make that class a wrapper. A cohesive, nontrivial responsibility or algorithm that is hard to test privately may be extracted into a concrete class with a
  meaningful public API for that responsibility; do not expose internals or create gratuitous wrappers for tests.
  -- A caller may accept a callback, lambda, functional interface, or callable type alias only for a stateless operation when that shorthand does not hide which component owns the
  operation or which caller invokes it.
  -- Reviewers must inspect the production implementation and direct callers before classifying an operation as stateless. A function without instance fields is not proof of a
  stateless operation.
  -- Reviewers must treat an operation as a component boundary when it reads configuration or global state, performs external I/O, owns timeout, retry, cache, or error translation
  policy, or coordinates an invariant or transaction.
* Avoiding False Equivalence (don’t merge superficially similar code with different contracts)
* Dispatch Mechanism Anti-patterns (avoid boolean parameters that select behavior, except for configuration. Local branches are appropriate when clearest; use polymorphism when
  justified by the Abstraction Costs / Over-Engineering rule. If only one behavior is needed, implement only that behavior.)
* Dependency Inversion Violations (high-level components use existing abstractions when they cover the use, rather than concrete implementations)
* Extensibility Design (reuse suitable existing extension points and abstractions needed now; do not add future-proofing or new extension points unless explicitly requested)
* Runtime Type Discrimination (move behavior into objects when polymorphism is justified)
* Factory Methods (avoid bottleneck factories; prefer in-class factory methods over separate Factory/Builder/Selector classes when variant count is low)
* Type hygiene & generics (no raw types; precise bounds; no unchecked casts/suppressions)
* Generic Abuse Check (don’t obfuscate contracts or shift errors to runtime)
* API design principles (interface segregation; class invariants; least surprise)
* Behavioral Contracts (implementations must fulfill interface contracts consistently)
* Backward Compatibility & Versioning (flag breaking changes; deprecations/migrations)
* No patch use: usage of `patch` in unit or integration tests is BANNED. The only exception is when patching external dependencies that we have no control over, but never patch our
  own code.

# 3. Reliability, Security, Performance & Delivery

**Summary instruction:** “Make failures explicit and safe; never leak; design for concurrency and real-world load; ship with tests and clean PR metadata.”

* Initialization & configuration (valid at construction; builders; no two-phase init; no hidden statics/global state; don't surface internals)
  -- Constructor Purity: No business logic in constructors (only validation and storage); no conditional logic to select implementations; no complex defaults based on other
  parameters; extract business logic to factory methods
* Concurrency & performance (thread-safe collections; immutables; avoid unnecessary `synchronized`; hot loops)
* Performance & Big-O Awareness (N² scans, unbounded collections - ensure state is cleared on removal, wasteful allocation - avoid redundant lookups before filtering)
* Prefer sets for binary state tracking (presence/absence) over dictionaries to reduce overhead.
* Resource management & memory (try-with-resources/contexts; no silent leaks; proper shutdown hooks)
* Resource acquisition order (only clean up what was acquired)
* Error handling & robustness (explicit flows; edge checks; specific catches; fail-fast messages; preserve required validation and error handling when moving or merging code)
  -- Validate at trust boundaries. Remove duplicate checks when the same invariant is already guaranteed at that point on every relevant path.
* Error Handling Recursion (don’t re-trigger the failing path in handlers)
* Exception Hygiene (chaining; capture variables, not live calls; no side-effects in formatting)
* Error Propagation (preserve cause/context; don’t mask)
* Security & Input Validation (injection risks; `PreparedStatement`; sanitize input; no hard-coded secrets)
* Preserve accessibility and hardware calibration when simplifying code.
* Test coverage & quality (cover new non-trivial behavior; deterministic; no sleeps/flakes; focused assertions)
* Use Orthogonal Arrays when planning combinatorial test scenarios with independent input factors; retain explicit positive, negative, boundary and error cases.
* Do not widen existing internals' visibility solely for test access; see **Avoid single-method wrapper classes** for extraction.
* PR Hygiene (title/why; tickets; before/after; visibility-drift audit)

# 4. Business Logic Correctness & Bug Hunting

**Summary instruction:** “Verify intended behavior, catch logic defects, and surface inconsistencies between code, comments, and domain intent.”

* Business rule correctness (does implementation match stated behavior, naming, and PR description)
* Conditional logic defects (wrong branch condition, inversion, missing branch, off-by-one)
* State and invariant validation (illegal transitions, stale flags, broken assumptions)
* Data correctness and integrity (silent corruption risk, wrong mapping/aggregation/joins, unit or timezone mismatches)
* Comment-code and test-code consistency (comments/tests contradict actual implementation)
* Edge-case logic and boundary behavior (null/empty, first/last element, reset/retry/reorder paths)
* Bug fixes (inspect all callers before changing a function; fix the root cause once in shared code when applicable)
* Regression sniffing (new code breaks legacy contract or domain workflow)

# 5. Scalability, Performance Impact & System-Wide Effects

**Summary instruction:** “Assess scaling behavior and blast radius across runtime, storage, and downstream systems.”

* Algorithmic scaling (N² hotspots, repeated scans, unnecessary recomputation)
* Runtime and memory pressure (allocation churn, leaks, unbounded collections, retained references)
* I/O and throughput impact (chatty network/storage calls, batching gaps, lock contention, queue backpressure)
* End-to-end system impact (upstream/downstream contract changes, fan-out failures, retry storms)
* Operational risk (latency SLO risk, capacity regression, deploy/rollback hazards)
* Multi-tenant/high-load safety (resource isolation, starvation/fairness, degradation behavior)
