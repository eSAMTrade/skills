**Java specifics**:

- Dependencies & config: minimal external libs; manage via Maven/Gradle; Constants should be kept in code (not config or env vars);
- Annotations: use standard annotations such as `@Override`; use JetBrains or Lombok annotations only when the project already declares those dependencies and conventions.
- Java baseline: follow the repository's declared version; if none is declared, default to Java 25 unless the task states otherwise
- Java 8+ idioms: prefer Stream/Optional over null checks; use CompletableFuture for async flows when needed
- Syntax: preview features are opt-in and should be suggested only when explicitly requested and environment-compatible. Use features supported by the baseline, including Gatherers where available.
- Concise Java syntax: avoid boilerplate loops that only fill, copy, box, or map values when standard Java APIs express the same intent clearly. For repeated initial
  values, prefer `new ArrayList<>(Collections.nCopies(itemCount, 0L))` over creating an empty list and adding `0L` in a loop. For pure array-to-list
  transformations, prefer streams such as `Arrays.stream(values).toList()` over a separate primitive array plus a `toList`
  helper. Keep explicit loops when they are clearer, stateful, or performance-critical.
- Use a private helper method instead of introducing a private class when the helper suffices.
- Result transformations: when a method validates and transforms data for a specific result type, return that result type directly instead of returning a
  primitive/intermediate container and converting it in a second helper. For example, prefer constructing `NormalizedValues` from the mapped stream result directly
  after validation.
- Validation scope: enforce invariants in constructors, records, and value-object factories. Before adding validation in aggregation, normalization, or conversion helpers,
  trace the invariant owner and call path. Retain checks for newly introduced arithmetic/range risks and invariants not guaranteed upstream.
- Parameters must be load-bearing: a method must not accept a parameter that is ignored, or only validated and then discarded. If the method reads the authoritative value from
  somewhere else (an exchange snapshot, a DB row, a fresh request), do not also accept it from the caller — take only what the caller alone can supply. An accepted-and-discarded
  parameter is indistinguishable from a used one at the call site, and the next person to touch the method will wire it back up. This matters most for quantities, prices, ids and
  versions, where the discarded value is a plausible-looking wrong answer.
- Default methods must not weaken the contract they document: if a `default` implementation cannot honour the guarantee stated in its own JavaDoc, it must throw
  `UnsupportedOperationException` rather than silently delegate to a broader or less safe operation. A default that "falls back" to the very behaviour the method exists to prevent
  turns an invariant into an opt-out that no compiler or test will flag.
- Encode invariants in types, not only in prose: when a rule can be enforced by the signature — omitting a parameter, a narrower type, a separate method — prefer that over
  documenting the rule and enforcing it with a flag, an enum switch, or a comment. Prose invariants survive exactly as long as the next refactor.
- Verify third-party API contracts before relying on them: for serialization codecs, schema-derived readers and framework bridges (Jackson, Vaadin `executeJs`, AMQP), confirm which
  types and shapes are actually accepted — from the library source, its bytecode, or a throwaway probe — instead of inferring it from the method signature. A signature that takes
  `Object` or a wide type frequently accepts far less at runtime, and the failure surfaces only in production.
- Trust adjacent warnings in the code you are changing: an existing comment explaining why something is done a certain way in this file is evidence about this codebase. If a change
  contradicts it, prove the comment is wrong before proceeding; a first error message that seems to disagree is not proof.
- Fix defect classes, not instances: after correcting a method, search for siblings that share its helper, shape, or call pattern, and either fix them in the same change or state
  explicitly why they are unaffected. Fixing one of a matching pair leaves the codebase inconsistent and the bug alive.
- Time handling: reuse the project's time-provider API when available. Otherwise use suitable Java APIs, such as an injected `java.time.Clock` for wall-clock time and `System.nanoTime()` for elapsed durations.
-  Documentation & examples: include usage examples for complex public utilities; ensure JavaDoc compiles without warnings
- Logging & Observability: use the project's logging framework and structured fields, correct log levels, and existing metrics or tracing hooks; flag any System.out.println used for logging purposes.
- Write concise JavaDoc only for relevant public APIs.
- Write code that does not produce compiler warnings; fix their causes and avoid hiding them with `@SuppressWarnings`.
- Interface naming: follow the project's existing convention of prefixing Java interface names with `I`, unless the touched package already has a stronger local convention.
- Style & conventions: respect repo formatter settings when configured; keep code, comments, and JavaDoc lines to 180 unless a
  file-local style is stricter, without artificial 100/120-column wrapping; and keep brace/newline placement consistent
- Method naming: methods should sound like actions or queries, not bare nouns. Avoid noun-only names such as `itemCount()`, `itemIndex(...)`, `rangeStart(...)`, or
  `itemConfigs(...)`; these read like record/component accessors and hide intent. Actual Java record component accessors and required interface overrides may keep
  their required names. Use `getX` for cheap retrieval or simple derived values (`getItemCount()`, `getRangeStart(...)`), `computeX`/`calculateX` for non-trivial
  math, indexing, aggregation, or formulas (`computeItemIndex(...)`, `calculateItemIndexAt(...)`), and `toX` for side-effect-free conversion to another
  representation (`toItemConfigs(...)`). Prefer `createX` or `buildX` for factory methods that assemble new result objects rather than convert the current value.
  Use `is`/`has`/`can`/`should` for boolean queries, `find`/`load`/`read`/`fetch` for lookup or I/O, and explicit verbs such as `apply`, `update`, `mark`, or
  `remove` for mutations. Do not hide side effects behind `get`, `compute`, `calculate`, or `to`.
- Generated sources: do not manually edit `src/main/generated`, `src/test/generated_tests`, or `src/systemTest/generated_tests` unless explicitly requested
- Test framework: use the project-declared framework and conventions; use JUnit/Mockito when the project uses them.
- Unit tests never wait for the clock. Do not use `Thread.sleep`, Awaitility, `Mockito.after(...)`, or any fixed or repeated delay that only lets time pass.
  - To check that an action happens, wait for its completion signal: `CountDownLatch`, `Future.get`, or `Mockito.timeout(...)`. The wait ends as soon as the signal arrives.
    The timeout value only stops a hung test.
  - To check that an action does not happen, do not wait and hope. Call the method that makes the decision and assert its result. If a worker thread would run the action,
    first wait until that thread has ended (`join(with-timeout)`, `awaitTermination(with-timeout)`), then assert.
  - To test code that reads the time, inject a controllable clock or the project's existing fake time provider and advance it in the test.
  - At the end of each test, stop every thread and executor the test started and wait until it has ended (`shutdownNow` + `awaitTermination`, or `join`) - with-timeout.
    No thread may keep running into the next test.
- Test placement: one test class per production class — `FooTest` for `Foo`. When adding tests for new or changed behavior of an existing class, ALWAYS add them
  to its existing test class (search for `<ClassName>Test` first); never create a parallel feature-suffixed test class (e.g. `FooNextLevelTest`, `FooPositionTest`)
  next to an existing `FooTest`. Follow the existing test class's conventions (helpers, parameterization/variant loops, naming) when extending it. Only introduce a
  separate class for a genuinely different test category with its own infrastructure (e.g. a component/backtest harness or a `src/systemTest` suite).
- NEVER-EVER do git commit operations without explicit ask! Never do git commit, push or pull without explicit instruction!
