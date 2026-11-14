---
name: py-dev
description: Implement and test Python changes, or check Python code quality when explicitly requested. Not for read-only debugging, diagnosis or explanation.
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. Read the repository root `AGENTS.md` if present. For review-only work, inspect the requested code and return findings; do not enter development, edit files or run tests unless
requested.

## Role and completion

Follow [Development](../orchestrate-subagents/SKILL.md#development), including [Failures & Escalation](../orchestrate-subagents/SKILL.md#failures--escalation). Assigned workers report their phase outcome, checks and limits to their immediate
caller, without claiming global completion. Without an assigned role, pursue the full task. If required delegation or independent completion checks are unavailable, report partial
progress, the missing capability and actionable briefs.

Before full implementation-task completion, an independent post-GREEN simplification reviewer must inspect the actual changed code and diff. Challenge debugging branches, helpers,
abstractions, duplicate logic, overrides and workarounds; check tests against the intended final public contract, not accidental intermediate behavior. Report findings; confirmed
defects follow [Failures & Escalation](../orchestrate-subagents/SKILL.md#failures--escalation). This check does not delay an assigned phase or leaf's local outcome report.

Use `tests/` for unit tests and `tests_integrations/` for integration tests, subject to actual repository layout. Integration tests use temporary directories and clean up; run
integration/system suites only when explicitly requested, including offline suites the repository labels integration. Report any confidence gap.

## Rules and quality

- Before planning, coding, testing or review,
  follow [Python instructions](../code-standards/references/python.instructions.md), [code design](../code-standards/references/code-design.md) and relevant repository instructions.
  Before writing tests, follow [Python test rules](../code-standards/references/py-test-rules.instructions.md). Follow the project-declared test framework; use `unittest` when no project convention is declared.
- Load the [instruction-compliance gate](../code-standards/references/instruction-compliance-gate.instructions.md) before edits and complete its final check within the assigned
  scope. Authors and reviewers inspect their own permitted actual diffs and report evidence. Follow [writing style](../writing-style/SKILL.md) for
  prose, [spec-writer](../spec-writer/SKILL.md) for technical documentation, and [file creation rules](../code-standards/references/file-creation-rules.instructions.md) before
  creating documentation or reports.
- Follow the project's provenance convention when it declares one. Where it uses `aicodesign`, annotate each newly authored class, function and method, including tests, with
  `@ai_draft("<actual LLM name and version>")`; annotate a new class and each new method separately. For an implementation-changed existing unit, downgrade existing provenance
  to `ai_draft` or add it if absent. Preserve provenance, including absence, for moves, copies, imports, renames and formatting without implementation changes. Do not add an
  undeclared provenance dependency or leave a placeholder literal.
- Provide meaningful, deterministic public-API tests for all new behavior and intended paths and branches, including positive, negative, boundary and error cases. Use equivalence
  partitioning to avoid redundant cases; do not test private members or expose internals for tests. If a private method is hard to test, extract its cohesive responsibility into a
  dedicated class with a meaningful public contract and test that API. Reuse test holders and prefer in-memory buckets unless testing filesystem behavior. Avoid sleeps and flaky
  tests.
- Within the assigned phase, use the active environment and repository-documented test runner; do not switch runners without a task-specific reason. Run configured lint and type
  checks for touched typed code and tests, including `mypy --strict` when mypy is used. For `uv`, use its documented command or `uv run --project ...`. Keep repository-specific
  runtime, path and lint settings in its `AGENTS.md`. Prefer scripts to multiline `python -c` commands.
- Follow the repository's declared Python baseline; the shared default is in the Python instructions. Use project-declared libraries and existing conventions for timestamps, time logic and iteration; use `tsx` and `streamerate` when the project declares and uses them. Prefer
   dataclasses for standard data when a simpler tuple is insufficient, `polars`/`pandas` only for massive datasets, `Path` for cross-platform paths and
  explicit top-level imports. Prefer Plotly for notebooks and analysis unless it cannot meet the requirement.
- Follow code design's abstraction and dispatch rules; place creation selection in a factory method or `@classmethod`, not `__init__`. Apply the linked typing and simplicity rules.
- Keep Git read-only. Remove temporary logging and comments. For requested PR-ready review, use the host's read-only review entrypoint and the canonical review loop. Report changed
  files, coverage, commands, results and review outcome; distinguish unit from business-functional coverage. Create Markdown reports only when explicitly requested.
