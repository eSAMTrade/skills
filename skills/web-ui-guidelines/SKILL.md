---
name: web-ui-guidelines
description: Review web UI code for interaction, responsive layout, performance, content, theming, and Vercel Web Interface Guidelines compliance.
---

Resolve links relative to this SKILL.md, including when installed in a plugin cache. Read repository UI instructions that govern the selected files.

# Web Interface Guidelines

Review the files named by the user (or the supplied file pattern) against only the focused references that match the code under review:

- [interaction.md](references/interaction.md) for forms, animation, navigation, state, touch, and interactive states.
- [layout.md](references/layout.md) for content sizing, images, safe areas, and overflow.
- [performance.md](references/performance.md) for rendering, loading, media performance, and hydration.
- [content.md](references/content.md) for typography and interface copy.
- [theming.md](references/theming.md) for dark mode and native control theming.

Read each applicable reference once per context. For a broad review, read all five; do not load the compatibility index as a second checklist. Keep the review read-only unless the
user separately requests fixes.

Inspect enough surrounding code to identify the actual interactive element, component state, and relevant styles. Report concise, actionable findings with exact file and line
locations. Follow the canonical document's output format and grouping exactly; do not add a preamble or a separate summary.

## Output format

Group findings by file using `file:line` and terse issue statements. Include only actionable issues; use `✓ pass` when a reviewed file has no findings.

```text
## src/Button.tsx

src/Button.tsx:42 - transition: all → list properties

## src/Card.tsx

✓ pass
```
