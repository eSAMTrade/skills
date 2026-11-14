---
name: orchestrate-subagents
description: Cost-aware orchestration for Codex and Claude. Route tasks to suitable models, parallelize independent work, and verify correctness while minimizing cost and latency.
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. The main thread orchestrates: plans, delegates, verifies, resolves ambiguity, and delivers results. Prioritize correctness, then cost and wall-clock time. Proceed without routine user approvals unless explicitly requested or essential requirements remain unresolved.

Specify `model` and `effort` (`reasoning_effort` in Codex) on every subagent launch when supported. Use available models or their closest equivalents.

## Models

Select models and effort from those available in the current runtime. Treat grades such as fast, mid, strong and top as relative capabilities, not fixed model aliases. Use the runtime's delegation tools and their supported options; if delegation or model selection is unavailable, use SINGLE where appropriate and report any resulting verification limits.

Choose grade/effort by judgment complexity, implementation complexity, ambiguity, risk, and verifiability — not fixed roles or quotas. Large mechanical work may use cheap models; subtle decisions need strong models. Architecture, security, concurrency, and high-risk financial/ML correctness require strong or higher. Stronger models may cost less per accepted task by avoiding failures.

## Agent Identity

Every agent, including the orchestrator (Tier 0), MUST begin its first message with exactly one identity line:

`Tier N · Role · Model · Effort · Goal: brief objective`

Example:
`Tier 1 · Developer · example-model · high · Goal: implement WebSocket parser`

Rules:
- Tier = parent's Tier + 1; orchestrator = Tier 0.
- State the assigned role, actual model, reasoning effort, and objective. Never invent unavailable runtime details; use `N/A` if unknown.
- Print the identity line once, at the very beginning of the first message; never repeat it.
- EVERY delegation brief MUST include the child's Tier, role, model, effort, goal, and this identity-line rule.
- Any agent delegating further MUST propagate the same rule recursively to its children, even when they cannot access this skill.

## Routing

Choose the simplest effective strategy:

- **SINGLE:** Small, serial, tightly coupled, or delegation-inefficient tasks.
- **LEAD-SIDEKICK:** Strong lead plans/decides/reviews; cheaper worker executes well-defined work.
- **PARALLEL-DAG:** Independent subtasks with stable interfaces and disjoint ownership.
- **CASCADE:** Cheap first attempt with reliable verification; escalate only when necessary.
- **CRITIQUE:** Independent strong review for high-risk logic or when explicitly requested.

Do not create unnecessary agents, roles, phases, or abstractions. Delegate early when boundaries are clear; avoid lead micromanagement. Re-route when difficulty changes. Optimize critical-path duration, not agent count. Launch independent ready tasks concurrently; avoid synchronization bottlenecks.

## Delegation

Each brief specifies:
- Agent identity: Tier, role, model, effort, goal, and mandatory first-line rule.
- Objective, expected behavior, and acceptance criteria.
- Relevant paths, interfaces, invariants, dependencies, and affected consumers.
- File ownership, prohibited changes, and verification commands.
- Deliverables: patch/paths, checks executed, evidence, unresolved issues.

Workers report to their launcher. No nested delegation unless beneficial. Share focused context and file paths, not full transcripts. Reuse useful persistent context; start fresh for independent review or polluted context. Preserve stable prompt prefixes/cache where supported; prefer completion notifications over polling.

Concurrent writers require disjoint ownership (including tests/fixtures) or isolated worktrees/checkouts and build outputs. Preserve unrelated changes.

### Scope & Contract Gate

Before implementation:
- Identify requested scope, affected shared classes/interfaces, their consumers, and existing contracts.
- Prefer local changes. A shared component affecting out-of-scope consumers is NOT implicitly authorized.
- If an out-of-scope change is unavoidable, explain its necessity and impact before requesting authorization.
- Never silently weaken observable guarantees (ordering, durability, consistency, delivery, compatibility) for performance or simplicity. Surface the tradeoff before adopting it.
- Do not invent performance thresholds or claim improvements without measurements.

## Development

The orchestrator defines a concise module-level plan and acceptance criteria. In delegated workflows it coordinates rather than duplicating implementation; SINGLE may implement directly.

Python/Java code authors load:
- [py-dev](../py-dev/SKILL.md)
- [java-dev](../java-dev/SKILL.md)

Use roles only when justified:
- **Architect (strong):** Complex design, interfaces, invariants.
- **Developer (by task):** Implementation and local checks.
- **Runner (deterministic/fast):** Independent execution of checks, no edits.
- **Reviewer (strong):** Independent semantic review, read-only.

### Baseline

Before any worker writes source or tests:
- Capture the initial repository snapshot: revision, tracked/staged/unstaged/untracked changes, relevant tests, and build configuration.
- Preserve existing changes; isolate baseline execution from concurrent writers.
- Run relevant baseline checks on the isolated snapshot, concurrently with preparation where possible.
- Record existing failures and verified environment limitations separately from new defects.

### Implementation & Tests

For substantial/high-risk business logic:

1. Identify existing contracts, affected consumers, tests, and baseline failures.
2. Define expected behavior, stable interfaces, and relevant lifecycle/state/time/error cases before implementation.
3. Prefer independently authored contract-based tests. Verify fixtures and obtain executable behavioral RED where applicable; freeze test expectations.
4. If missing APIs prevent compilation, test through existing interfaces or introduce only agreed signatures without business logic before establishing behavioral RED.
5. Implement without changing frozen expectations. Authors run applicable local lint, compile, and tests before handoff; local checks never replace independent verification.
6. At the first stable snapshot, run new tests AND existing tests directly affected by changed behavior/contracts. Diagnose regressions before proceeding to expensive full verification.
7. Verify GREEN with regression and configured checks on the integrated snapshot.

For small/mechanical work, skip unnecessary design/TDD phases but verify the result.

Prefer deterministic tools over LLM agents for running tests. Run relevant existing unit and safe offline integration checks; live services/network require authorization. Independent verification is required when risk warrants it, but need not use another LLM. Passing tests alone does not prove semantic correctness.

Early diagnostic review is allowed on stable snapshots for high-risk changes, in parallel with tests when outputs are isolated. It does not replace final verification or requested PR review.

## Failures & Escalation

Diagnose before escalating:

1. **Environment/tool failure:** Fix the blocker; retry without stronger models.
2. **Unclear brief:** Clarify and retry at the same model/effort.
3. **Localized defect:** Prefer a targeted fix by the existing author, then verify.
4. **Repeated failure/reasoning limit:** Increase effort/model or request independent strong diagnosis.
5. **Unresolved high-risk issue:** Escalate to top when available; otherwise report limitations.

Avoid automatic fresh-agent replacement, blind escalation, repeated full-task retries, and endless correction loops. Preserve valid work. Group related findings for the same artifact/owner into one correction handoff; do not block independent branches.

Compare unexpected failures against baseline. Distinguish behavioral failures from compilation, fixture, and environment failures. Add regression tests for demonstrated gaps. Change existing tests only for proven contract errors. Never weaken assertions, suppress failures, or change expectations merely to pass.

Preserve evidence before reruns: command, snapshot, exit code, full logs, test reports, and exclusions, using unique run artifacts where supported.

Rerun affected checks after corrections. Invalidate previous checks/reviews whenever their relevant inputs change; if dependencies are uncertain, rerun. Before delivery, report which checks remain valid for the final snapshot and which were not run.

Accept only results supported by sufficient evidence.

## PR-ready Review

Perform formal PR-ready review ONLY when requested.

Review independently and read-only on a stable, verified snapshot. Include task-related committed, staged, unstaged, and untracked changes within scope.

Report inspected paths/snapshot, findings, severity, and limitations. Consolidate related findings before correction. Correct significant confirmed findings, rerun affected checks, and review the updated snapshot. Never accept unresolved significant findings or claim unseen files were reviewed.

## Optimization

When measurable, track:
- Functional success, regressions, and cost per accepted task (including retries/review).
- Wall-clock duration, critical path, and delegation overhead.
- Model/effort usage, cache efficiency, escalations, and integration conflicts.

Benchmark multi-agent configurations against SINGLE at different effort levels. Adopt optimizations only when representative results justify them.
