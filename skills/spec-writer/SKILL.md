---
name: spec-writer
description: Write or revise specifications, design notes, and technical documentation with verifiable contracts and explicit unresolved decisions. Use for document creation and cleanup, not production-code changes.
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. Before working on a repository, read its root `AGENTS.md` if it exists, regardless of the
current working directory.

Produce an authoritative document that a reader can implement or verify without guessing.

Follow [writing style](../writing-style/SKILL.md) if not already in context. The rules below add document-specific guidance for specifications, design notes, architecture
documents, READMEs, and regression records. Apply formal-contract rules only to normative requirements. When reviewing, preserve the caller's review scope and permissions.

1. Read the whole document and the references needed for the edit. Follow repository instructions governing that document. Prefer updating the existing authoritative document;
   create a file only when requested or needed for the task.
2. Establish whether the document describes existing behavior or a proposed contract. Check relevant code, tests, or incident evidence for claims about implementation; flag
   disagreements with intended behavior instead of silently choosing one as correct.
3. Make the requested changes in place. Keep edits within the document's purpose and the user's scope; do not change production code or behavior.
4. Run the applicable checks below, then report substantive changes and deletions with reasons, verification performed, and unresolved questions. Claim consistency only to the
   extent checked.

## Document rules

- Describe behavior in present tense and stay within the documented component's ownership; refer to other components' contracts without explaining their internals.
- Use named pointers to existing headings, decisions, or functions, never section/rule numbers or vague "earlier" references.
- Use tables for closed comparisons of states, outcomes, fields, commands, or modes when they help check completeness.
- For quantitative examples, use realistic units and values, introduce with `Suppose ...`, and walk through the case.
- Put a rule before its separate rationale, labeled `**Why.**`.

## Formal contracts

- Use **must** for required behavior (violations are incorrect), **must NOT** for forbidden behavior, **may** for an implementation choice, and **recommended** for a default
  requiring a reason to depart. Avoid `shall`, `is supposed to`, `would normally`, `should`, and `ideally` as obligation words.
- Mark unresolved semantics `AMBIGUOUS:`, `ASSUMPTION:`, or `UNCLEAR:` and say exactly what is unknown. Resolve blocking ambiguity through source verification or the user.
- Keep each requirement in one owning location: rewrite changes in place, remove superseded rules, and reference the owning heading elsewhere. Test sections may list covered cases
  without repeating required outcomes.
- State the current intended contract directly. Keep superseded-design history, implementation status, and incident evidence in sections intended to report them, outside normative
  requirements. Preserve meaningful runtime distinctions such as stale or previous state.

## Checks

- Verify named pointers resolve, terminology is consistent and defined, tables have consistent columns, code fences balance, and claims respect component ownership.
- For changed requirements, search the whole document for duplicate or conflicting obligations and implications; check obligation words and the behavioral elements defined in
  writing-style. Check that historical design or build commentary has not entered the contract.
- Compare with the pre-edit version for unintended losses; account for removed requirements, identifiers, numeric constants, and ALL-CAPS names. Keep a scratch copy when no
  reliable baseline exists.

Keep Git read-only; do not commit, push, reset, or restore.
