# Interaction

Use this reference for forms, animation, navigation, state, touch interaction, and hover states.

## Forms

- Inputs need `autocomplete` and a meaningful `name`.
- Use the correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`.
- Never block paste with `onPaste` and `preventDefault`.
- Keep the submit button enabled until the request starts and show progress while it runs.
- Show errors next to the relevant fields and focus the first error on submit.
- Placeholders end with `…` and show the expected pattern.
- Use `autocomplete="off"` on non-auth fields to avoid password-manager triggers.
- Warn before navigation with unsaved changes (`beforeunload` or a router guard).

## Animation

- Animate `transform` and `opacity` only when possible.
- Never use `transition: all`; list properties explicitly.
- Set the correct `transform-origin`.
- For SVG, put transforms on a `<g>` wrapper with `transform-box: fill-box` and `transform-origin: center`.
- Make animations interruptible so user input can take effect immediately.

## Navigation and state

- Reflect filters, tabs, pagination, and expanded panels in URL query parameters when they should be shareable.
- Use `<a>` or `<Link>` for navigation so normal browser link actions work.
- Deep-link stateful UI when its state should survive refresh or sharing.
- Destructive actions need a confirmation step or an undo window.

## Touch and interactive states

- Set `touch-action: manipulation` where it prevents an unwanted double-tap delay.
- Set `-webkit-tap-highlight-color` intentionally.
- Use `overscroll-behavior: contain` in modals, drawers, and sheets.
- During drag, disable text selection and mark dragged elements inert where supported.
- Provide a tap or click alternative for drag, swipe, pinch, and path gestures unless the gesture is essential.
- Use `autoFocus` sparingly: desktop only, one primary input, and never by default on mobile.
- Buttons and links need a visible hover state with stronger contrast than the resting state.

## Anti-patterns

- `onPaste` with `preventDefault`
- `transition: all`
- Inline `onClick` navigation without `<a>` or `<Link>`
- Destructive actions with no confirmation or undo
- Gesture-only actions with no tap or click alternative
