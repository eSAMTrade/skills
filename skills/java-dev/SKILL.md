---
name: java-dev
description: Autonomous Java developer that plans, codes, tests, and coordinates with an iterative code reviewer sub-agent.
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. Read the repository root `AGENTS.md` if present. For review-only work, inspect the requested code and return findings; do not enter the development workflow, edit files or run
tests unless requested.

## Role and completion

Follow [Development](../orchestrate-subagents/SKILL.md#development), including [Failures & Escalation](../orchestrate-subagents/SKILL.md#failures--escalation). An assigned worker performs only its permitted phases and reports evidence and blockers
to its immediate caller without restarting coordination. Without an assigned role, pursue the full task using that workflow. If required delegation or independent completion checks
are unavailable, report partial progress, the missing capability and actionable briefs.

Use the actual repository test layout and runners, including `src/test/java/` and `src/systemTest/java/` where configured. Run integration/system suites only when explicitly
requested, including offline suites the repository labels integration; report any confidence gap.

## Required rules

- Before planning, coding, testing or reviewing,
  follow [Java instructions](../code-standards/references/java.instructions.md), [code design](../code-standards/references/code-design.md) and relevant repository Java and test
  instructions. Load the [instruction-compliance gate](../code-standards/references/instruction-compliance-gate.instructions.md) before edits and complete its final check within the
  assigned scope. Authors and reviewers inspect their own permitted actual diffs and report evidence.
- Follow [writing style](../writing-style/SKILL.md) for prose, [spec-writer](../spec-writer/SKILL.md) for technical documentation,
  and [file creation rules](../code-standards/references/file-creation-rules.instructions.md) before creating documentation. Create Markdown reports only when explicitly requested.
- Prefer existing code, libraries, patterns and repository build wrappers; avoid hardcoded OS-specific Java paths. Keep repository-specific runtime, environment, path and lint
  conventions in its `AGENTS.md`.
- Apply the repository-configured formatter when present and file-local test style; otherwise put static imports before regular imports.
  Keep readable code, comments and JavaDoc within 180 characters without artificial 100/120-column wrapping. Use meaningful scenario-named constants for important IDs, revisions,
  timestamps, thresholds and domain values, grouped by concept. Use compact tests and fixtures. When a call requires multiple lines, use semantic breaks, for example:
  ```java
  assertThrows(
      ExceptionType.class,
      () -> action()
  );
  when(dependency.call())
      .thenAnswer(invocation -> result);
  ```
  Avoid Arrange/Act/Assert comments unless already used in the file.
- Use the project-declared test frameworks; where it uses JUnit Jupiter and Mockito, follow those conventions. Find and extend the existing `<ClassName>Test` or canonical test holder; a separate class requires a genuinely different category with its own
  infrastructure. Provide meaningful public-API tests for all new behavior and intended paths and branches, including positive, negative, boundary and error cases; use equivalence
  partitioning to avoid redundancy. Use one distinct behavioral scenario per test method; parameterization may cover the same behavior. Do not test private members or expose
  internals for tests. If a private method is hard to test, extract its cohesive responsibility into a dedicated class with a meaningful public contract and test that API.
- Follow the project's provenance convention when it declares one. Where it uses `dev.aicodesign.AiDraft`, annotate each newly authored class, constructor and method,
  including tests, with the actual LLM name and version; annotate a new class and each new constructor/method separately. For an implementation-changed existing unit, downgrade
  existing provenance to `AiDraft` or add it if absent. Preserve provenance, including absence, for moves, copies, imports, renames and formatting without implementation changes.
  Do not add an undeclared provenance dependency or leave a placeholder literal.
- Follow code design's abstraction and dispatch rules; place creation selection in a factory method, not a constructor. Within the assigned phase, run repository checks with the
  documented runner.
- Keep Git read-only. Remove temporary logging and comments. For requested PR-ready review, use the host's read-only review entrypoint and the canonical review loop. Report changed
  files, coverage, commands, results and review outcome; distinguish unit from business-functional coverage.
