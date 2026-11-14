---
name: writing-style
description: Write, explain, rephrase, or review any prose with clear wording and precise meaning, including replies, questions, PR descriptions, comments, docstrings, and documents.
---

Make the meaning clear enough that the reader can act without guessing. Preserve the task's purpose and format. Load this skill once per context.

- Use short sentences, one idea each, active voice, and concrete verbs describing what happens. Prefer `reads`, `sends`, or `returns` over vague or inflated `handles`, `manages`,
  `processes`, `leverages`, `facilitates`, or `orchestrates` when accurate.
- Use one exact term per concept; define abbreviations, version shorthand, and invented compounds before use. Preserve real identifiers and domain/protocol terms. Keep actors,
  actions, results, identities, states, events, and ownership distinct.
- Explain behavior through its actor, trigger, exact condition, observable result, and lifecycle ownership. Define baselines for `current`, `matching`, `newer`, or `previous`.
  Components act; messages contain data unless explicitly modeled as active.
- Distinguish confusable identifiers before drawing conclusions: who assigns each, what it identifies, whether it survives updates/replacements/retries, and the documented link
  between related records. When true, distinguish a client-tracked logical request/object from a system-created record/version.
- Match claims to evidence. Make uncertainty and correctable assumptions explicit; never invent actors, causes, invariants, or outcomes. Remove misleading metaphors and unsupported
  causal claims.
- In conversation, give enough context to answer and ask one focused question at a time unless the workflow defines a batch. Keep guesses visible; do not impose document formatting
  or formal contract checks.
- In comments/JavaDoc/docstrings, explain non-obvious contracts, invariants, or reasons rather than signatures or obvious flow. Describe inputs, actions, and exact
  return/ignore/retry/throw conditions in reader order; verify against nearby code, including claims of thread safety or atomicity. Inline comments explain why a business rule,
  algorithm, or workaround exists. No decorative separators, banners, ASCII art, section headers, or commented-out code. TODOs need an owner and a ticket or date.
