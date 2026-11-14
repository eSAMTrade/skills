# Layout and media

Use this reference for content sizing, images, safe areas, and overflow.

## Content handling

- Text containers handle long content with `truncate`, `line-clamp-*`, or `break-words`.
- Flex children need `min-w-0` when text must truncate.
- Handle empty states instead of rendering broken UI for empty strings or arrays.
- Test user-generated content at short, average, and very long lengths.

## Images

- Give `<img>` elements explicit `width` and `height` to prevent layout shift.
- Use `loading="lazy"` for below-fold images.
- Mark an above-fold critical image with `priority` or `fetchpriority="high"`.

## Safe areas and layout

- Full-bleed layouts account for notches with `env(safe-area-inset-*)`.
- Prevent unwanted horizontal scrollbars and fix the content overflow at its source.
- Prefer flex and grid over JavaScript measurement for layout.
