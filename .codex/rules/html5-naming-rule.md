# HTML5 Naming & Syntax Rules (W3Schools HTML5 Syntax)

This document defines the required **HTML5 naming and syntax conventions** for generated HTML.

Source (only): `https://www.w3schools.com/hTml/html5_syntax.asp`

## Document basics

- Always declare the document type as the first line:
  - `<!DOCTYPE html>`
- Never skip the `<title>` element (it is required in HTML).
- Strongly prefer including `<html>` and `<body>` tags (even though a page can validate without them).
- Add the `lang` attribute to the `<html>` element (for example: `<html lang="en-us">`).
- Define character encoding early (for example: `<meta charset="UTF-8">`).
- Include viewport metadata in all web pages:
  - `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

## Element and attribute naming

- Use **lowercase element names** (for example `<body>`, not `<BODY>`).
- Use **lowercase attribute names** (for example `href`, not `HREF`).
- Always **quote attribute values** (for example `class="striped"`, not `class=striped`).

## Closing elements

- Close all HTML elements (even where optional), for example always close `<p>`.
- Empty elements may be written without a closing slash (`<meta charset="utf-8">`), or with one (`<meta charset="utf-8" />`).
  - Keep the `/` if XML/XHTML software is expected to access the page.

## Whitespace and formatting

- No spaces around `=` in attributes:
  - Prefer: `<link rel="stylesheet" href="styles.css">`
  - Avoid: `<link rel = "stylesheet" href = "styles.css">`
- Avoid long code lines that require horizontal scrolling.
- Use blank lines and indentation only with a reason:
  - Use blank lines to separate large or logical blocks.
  - Use **two spaces** for indentation; do not use tabs.

## Images

- Always specify `alt` for images.
- Also specify `width` and `height` for images to reduce flickering (layout shifts).

## External resources

- Linking CSS: use simple syntax; the `type` attribute is not necessary:
  - `<link rel="stylesheet" href="styles.css">`
- Loading external JavaScript: use simple syntax; the `type` attribute is not necessary:
  - `<script src="myscript.js">`

## Case sensitivity note (IDs / selectors)

- Be consistent in attribute values used by JavaScript and CSS (for example `id` values), because inconsistent casing can cause JavaScript selector mismatches (example shown in the source page).

## File naming rules

- Use **lowercase file names** to avoid issues on case-sensitive servers.
- File extensions:
  - HTML files: `.html` (or `.htm` allowed)
  - CSS files: `.css`
  - JavaScript files: `.js`

