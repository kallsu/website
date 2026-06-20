# Feature: Remove Activities From Homepage

## Requirements

- Remove the `Activities` link from the main navigation in `src/index.html`
- Remove the `Activities` content block from the homepage body in `src/index.html`
- Update `src/index.md` so it no longer documents the Activities section
- Preserve the rest of the homepage content, navigation, and contact links

## Business Rules

- The homepage must remain static HTML5/CSS3 with no JavaScript changes
- Internal navigation must not reference removed content
- Markdown content should stay aligned with the HTML source

## Acceptance Criteria

- The top navigation no longer contains an Activities link
- The homepage body no longer renders the Activities section
- `src/index.md` no longer lists the Activities section
- Remaining homepage links and contact information still render as before
