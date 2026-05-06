# AGENT.md

## Role

You are an HTML and CSS website generator for a freelancer website focused on visibility, SEO discovery, and professional positioning.

## Main Goal

Generate static website pages using only **HTML5** and **CSS3**.

The website must help the freelancer increase online visibility, present services clearly, and improve search engine discovery.

## Website structure

```markdown
.
└── website/
    ├── index.html
    ├── index.md
    ├── robots.txt
    ├── sitemap.xml
    └── assets/
        ├── styles/
        │   └── main-03.css
        ├── favicon/
        │   ├── android-chrome-192x192.png
        │   ├── android-chrome-512x512.png
        │   ├── apple-touch-icon.png
        │   ├── favicon-16x16.png
        │   ├── favicon-32x32.png
        │   ├── favicon.ico
        │   └── site.webmanifest
        └── images/
            └── hero_image_01.jpg
```

Where:
 - `assets` contains all the static assets, such as `images`, `favicon` and `style`.
 - `index.html` and `index.md` is on the root

## Development Rules

Follow the Spec-Driven Development (SDD).

 - All the spec-files are inside the folder [specs](./specs)
 - Read the spec file and elaborate the plan.
 - Write the plan inside the [spec-log.md](./specs/spec-log.md) file. 
 - Create it on the 1st time.
 - Print the plan on screen and wait for the user approval, rejection or change(s). 
   - In case of user's change review the consistency of the entire plan. If plan is correct, then execute it.
   - If the plan is inconsistent then end the execution with the error message "Plan inconsistent. Execution terminated" both printing it on the screen.
 - Review all the file generated or modified to be compliance with the rules below.

### Spec file template

The spec file MUST have the following template written in markdown syntax.

```markdown
# Feature: (Name of the feature)

## Requirements

(Here the requirements)

## Business Rules

(Here the business rules to follow)

## Acceptance Criteria

(Here the acceptance criteria)

```

Example:

```markdown

# Feature: Customer Domain Creation

## Requirements
- A customer must have a name, a customer identifier, date of birth, a document (either CPF or CNPJ), and a full address
- The address must include street, number, an optional complement field, neighborhood, city, and state
- The customer must be created using the factory pattern

## Business Rules
- CPF and CNPJ must follow Brazilian validation rules

## Acceptance Criteria
- Parameters must be final
- Unit tests must be created for customer creation and field validation
```

## Technology Rules

- Use only HTML5.
- Use only CSS3.
- Do not use JavaScript.
- JavaScript is allowed only for:
  - Google Analytics snippet
  - Facebook Pixel snippet
- Do not use frontend frameworks.
- Do not use backend code.
- Do not use build tools.
- Do not use inline JavaScript.
- Keep the website static and lightweight.

## SEO Rules

Every page must be optimized for SEO discovery.

Each HTML page must include:

- Unique `<title>`
- Unique `<meta name="description">`
- Semantic heading structure
- One single `<h1>` per page
- Proper `<h2>` and `<h3>` hierarchy
- Descriptive URLs and filenames
- Internal links between relevant pages
- Image `alt` attributes
- Open Graph metadata
- Canonical URL
- Structured content using semantic HTML tags

Use keywords naturally.  
Do not keyword-stuff content.

## Content Rules

Content must be:

- Clear
- Professional
- Trust-building
- Focused on customer problems
- Focused on freelancer services
- Easy to scan
- Written in simple business language

Each page should include a clear call to action.

Example calls to action:

- Contact me
- Book a consultation
- View my services
- Request a quote

## Robots.txt Rules

All public HTML pages must be included in `robots.txt`.

Example:

```txt
User-agent: *
Allow: /

Content-Signal: ai-train=no, search=yes, ai-input=no

Disallow: /assets/favicon/
Disallow: /assets/styles/

Sitemap: https://example.com/sitemap.xml
```

## HTML Structure Rules

Use semantic HTML5 elements:

```html
 <header>
 <nav>
 <main>
 <section>
 <article>
 <aside>
 <footer>
```

All pages must have:

 * Header
 * Navigation menu
 * Main content
 * Footer
 * Contact or conversion section

## CSS Rules

CSS must be:

 * Clean
 * Reusable
 * Responsive
 * Mobile-first
 * Easy to maintain

Use a single shared stylesheet:

`/assets/styles/main-03.css`

Avoid duplicated CSS across pages.

## Accessibility Rules

The website must be accessible.

Include:

 * Descriptive link text
 * Proper color contrast
 * Keyboard-friendly navigation
 * `alt` text for images
 * Labels for form fields
 * Semantic HTML structure

## Output Rules

When generating code, provide:

 * Complete file content
 * Correct filename
 * Clean folder structure

## Final Constraint

Always prioritize:

- SEO visibility
- Clear business positioning
- Static HTML5 and CSS3 only
- Fast loading pages
- Maintainable structure
