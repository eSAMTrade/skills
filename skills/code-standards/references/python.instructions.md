**Python specifics**:
- Align with Google Python Style Guide's structural tips (e.g., function design, class setup, and Pythonic usage), but skip formatting or whitespace—focus on high-level quality and maintainability.
- Dependencies & config: minimal third-party libs; externalize settings; no hidden constants
- Style & conventions: PEP8/PEP257 compliance; 180 char max line length (project setting); follow project lint rules;
  -- Parameter formatting: if 2-4 simple parameters fit in 180 chars, keep on one line; otherwise each parameter on separate line with proper indentation
  -- Semantic decorators: when editing Python code, add applicable decorators such as `typing.override`, `@staticmethod`, `@classmethod`, and `@property`; do not add decorative or no-op decorators.
  -- Compact formatting: prefer one-line imports, function/method signatures, and function calls whenever they fit within the 180-character project limit.
  -- Trailing commas: remove trailing commas from imports, function parameters, and call arguments when their only effect is forcing formatters such as `black`/`isort` to keep code split across multiple lines. If formatter output still keeps a short construct multiline, treat that as a style/config issue to resolve instead of leaving avoidable vertical formatting.
  -- Default arguments: avoid by default. Use default parameter values only when omission is a clear, current API/domain contract. If a value is required for correctness, make it a required parameter or derive it from injected instance state; do not hide it behind `None` sentinels or fallback defaults.
- Logging & Observability: ensure use of structured logging (logging module), correct log levels, flag any print() statements used for logging purposes, and hooks for metrics or tracing.
- Prefer project-declared libraries and established conventions for data, iteration and time. Use `streamerate` or `tsx` when the project declares and uses them; otherwise use suitable existing or standard-library tools. Flag heavy new dependencies for discussion.
- Follow the repository's declared Python baseline; if none is declared, default to Python 3.12 compatibility unless the task states otherwise.
- For internal logic, use a tuple instead of introducing a private dataclass when the tuple suffices.
- Shared abstractions: use concrete classes / `ABC` first.
  - Do not introduce `Protocol` for repo-owned abstractions. Use a named concrete class or an `ABC` for a repo-owned component boundary.
  - If behavior is shared across internal classes, prefer:
    1) an `ABC` with `@abstractmethod`, or
    2) a concrete superclass with shared implementation.
  - For interface-style refactors, require a pre-flight check that `Protocol` is not newly introduced for internal abstractions. If structural typing is unavoidable for an external boundary, document why the concrete or `ABC` option is impractical.
  - Do not override or redeclare existing base-class attributes in subclasses just to mirror a parent member. If a member already exists in the base, keep it there and only add new members in the subclass unless behavior is intentionally changed.
- Type hygiene: complete and correct type hints; no implicit `Any`; no uninformative `Any` or `object` in new or touched annotations unless crossing an unavoidable external boundary.
  -- Replace broad boundary types with concrete classes, dataclasses, `TypedDict`, precise type aliases, `ABC`, or explicit domain value types that describe what the code actually expects.
  -- A `Callable[...]` annotation describes only the call shape. It must not be used as evidence that a callback is the correct dependency boundary; apply **Avoid single-method
  wrapper classes** before introducing one.
  -- When touching a contract or adjacent implementation that already uses `Any`/`object`, narrow it as part of the change if the expected shape is knowable from call sites or domain models.
  -- Do not use `cast`, runtime type checks, or wrapper types to hide unclear contracts. Prefer making the producer, consumer, and test double signatures precise.
  -- Getter Methods: Don't flag well-documented getter/accessor methods that have clear purposes as violations of encapsulation when they're providing intentional access to internal state.
- **Docstring coverage** (wording belongs to the shared writing style loaded by the canonical skill):
  -- Follow project's minimal documentation approach: avoid docstrings for trivial getters/setters
  -- Docstrings required only for: public APIs, complex algorithms, non-obvious business rules
  -- Remove docstrings that simply restate type hints or method names (e.g., """Get user name""" for get_user_name() -> str)
  -- Consistent style: if codebase uses minimal commenting, maintain that pattern
  -- Type hints replace most parameter/return documentation needs
- Type-Safe Refactoring: Avoid introducing ambiguous return types (Any) or runtime casting. Maintain precise type signatures when refactoring methods. Don't sacrifice static type checking for DRY.
- Private-helper refactors: do not preserve old private call sites with compatibility defaults. Update private call sites and tests to the new explicit contract.
- Return Type Clarity: Methods should have clear, specific return types. Flag any solution that mixes return types based on string parameters or other runtime values.
- Visibility & naming (Python): adopt consistent underscore prefixes to signal intent, not enforce access. Public: no underscore (stable API). Protected-internal: single underscore _name (internal to module/package or subclass use; subject to change). Private-to-class: double underscore __name (name-mangled; only when you must prevent accidental override in subclasses). Don’t mix scopes for the same symbol across hierarchy.
- Attribute scope clarity: don’t declare mutable class attributes that are later shadowed by per-instance assignments; explicitly model intent with either instance attributes initialized in init/setUp or class attributes marked ClassVar without instance rebinding. Prefer factory/abstract methods to make initialization points explicit. Use clear names without leading underscores unless truly non-public.
  -- Pick one scope and stick to it: If a base class exposes state to subclasses, model it as protected instance state (single underscore) initialized in the base, or as a protected factory method the base calls. Do not define a mutable class attribute and then reassign it per-instance in subclasses.
  -- No shadowing class -> instance: Mutable class attributes that are later rebound on instances are forbidden. If you need per-test values, move the value to an instance attribute initialized in __init__/setUp, or provide it via a protected factory (_create_*) that subclasses override.
  -- Dependency injection over mutation: If the value is a dependency, prefer passing it into the base’s constructor/setUp or overriding a factory method; don’t mutate a base attribute from a subclass.
- Readability & clarity:
  -- No inner functions (nested defs) for core logic; Prefer top-level or class-level helpers for shared logic. Allowed only when:
  --- Used in tests (unit or integration tests)
  --- Implementing a decorator or higher-order function where the wrapper must close over parameters;
  --- Creating a short callback passed immediately to a single API (e.g., key functions, small predicates) where a lambda would be too cramped but a top-level function would be noise.
  --- A closure is required to bind a small amount of immutable context without introducing a class or partial.
  -- Entrypoints: prefer an explicit callable entrypoint (for example `main()`) instead of keeping executable behavior only inside `if __name__ == "__main__":`.
  -- Avoid in-process `runpy.run_module(..., run_name="__main__")` when the module may already be imported or when execution initializes global state or owns resources such as logging handlers, cwd changes, temp files, or signal handlers. Use it only when `python -m` semantics are the behavior under test; otherwise prefer direct function calls or subprocess isolation.
  -- Class-centric helper organization (Java/Python consistency): Module-level helper functions that are tightly coupled to a single class should be encapsulated inside that class as private static methods (`@staticmethod`) or class methods, not left at module level. Flag new module-level functions unless they are: (a) genuinely part of the module's public API, or (b) clearly reusable across multiple classes/modules. This codebase intentionally favors Java-like class-centric organization for consistency across both languages.
  -- Code formatting: try to fit function/method defitionions and calls within the same line of 180 chars when possible. If not, break parameters into multiple lines with proper indentation for readability.
    - *WRONG:* 
        ```def _load_hour_index_rows_entry(
                  self,
                  hour_start: iTS,
                  range_start_ts: iTS,
                  range_stop_ts: iTS,
                  lookback_minutes: int
          ) -> tuple[iTS, list[dict[str, int | float | None]]]:
              ...
        ```
    - *RIGHT:*
        ```def _load_hour_index_rows_entry(self, hour_start: iTS, range_start_ts: iTS, range_stop_ts: iTS, lookback_minutes: int) -> tuple[iTS, list[dict[str, int | float | None]]]:
              ...
        ```
