# Performance and rendering

Use this reference for rendering, loading, media performance, and hydration.

## Performance

- Virtualize large lists (more than 50 items), or use `content-visibility: auto` where it fits the UI.
- Do not read layout in render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, or `scrollTop`).
- Batch DOM reads and writes; avoid interleaving them.
- Prefer uncontrolled inputs. Controlled inputs must remain cheap per keystroke.
- Add `<link rel="preconnect">` for CDN and asset domains.
- Preload critical fonts with `<link rel="preload" as="font">` and use `font-display: swap`.
- Prefer `<video autoplay muted loop playsinline>` over an animated GIF and provide a still alternative.
- For short non-essential loops, provide a compressed video source and a still fallback.

## Hydration safety

- Inputs with `value` need `onChange`; use `defaultValue` for uncontrolled inputs.
- Guard date and time rendering against server/client hydration mismatches.
- Use `suppressHydrationWarning` only where it is truly needed.

## Anti-patterns

- Large arrays rendered with `.map()` without virtualization
- Layout reads in render
- Animated GIF where compressed video is suitable
